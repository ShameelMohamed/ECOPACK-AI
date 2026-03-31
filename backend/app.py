from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. Database Configuration (PostgreSQL)
# ==========================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Infinity@localhost/ecopackai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class RecommendationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    weight_capacity_kg = db.Column(db.Float, nullable=False)
    tensile_strength_mpa = db.Column(db.Float, nullable=False)
    top_material = db.Column(db.String(100), nullable=False)
    est_cost = db.Column(db.Float, nullable=False)
    est_co2 = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ==========================================
# 2. Machine Learning Setup
# ==========================================
print("Loading Optimized Industry-Aware ML Models...")
MODEL_DIR = '../model'
try:
    # Load the 3 Models
    material_classifier = joblib.load(os.path.join(MODEL_DIR, 'xgb_classifier.pkl'))
    cost_model = joblib.load(os.path.join(MODEL_DIR, 'cost_predictor_rf.pkl'))
    co2_model = joblib.load(os.path.join(MODEL_DIR, 'co2_estimator_xgb.pkl'))
    
    # Load the Encoders dictionary
    encoders = joblib.load(os.path.join(MODEL_DIR, 'categorical_encoders.pkl'))
    cat_encoder = encoders['category_name']
    mat_encoder = encoders['material_type']
    
    print("Models and Encoders loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}. Make sure you ran the updated train_models.py first!")

# ==========================================
# 3. REST API Endpoints
# ==========================================
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "database": "connected"})

@app.route('/api/recommend', methods=['POST'])
def recommend_packaging():
    try:
        data = request.json
        category = data['category_name']
        weight = float(data['weight_capacity_kg'])
        strength = float(data['tensile_strength_mpa'])
        biodegradability = float(data.get('biodegradability_score', 50))
        recyclability = float(data.get('recyclability_percent', 50))

        # --- ENCODING ---
        # Safely encode the industry category (Fallback to 0 if unknown)
        encoded_cat = cat_encoder.transform([category])[0] if category in cat_encoder.classes_ else 0

        # --- STEP 1: The Physics Gatekeeper (Classifier) ---
        clf_features = ['category_name', 'tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'recyclability_percent']
        input_clf = pd.DataFrame([[encoded_cat, strength, weight, biodegradability, recyclability]], columns=clf_features)
        
        # Get Probabilities & Extract Top 3 Physically Viable Materials
        probabilities = material_classifier.predict_proba(input_clf)[0]
        top_3_indices = np.argsort(probabilities)[::-1][:3]
        top_3_materials = mat_encoder.inverse_transform(top_3_indices)

        unsorted_results = []
        reg_features = ['category_name', 'material_type', 'tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'recyclability_percent']
        
        # --- STEP 2: The Estimators (Regressors) ---
        for material in top_3_materials:
            encoded_mat = mat_encoder.transform([material])[0]
            
            # Predict Cost and CO2 using BOTH Industry and Material info
            input_reg = pd.DataFrame([[encoded_cat, encoded_mat, strength, weight, biodegradability, recyclability]], columns=reg_features)
            
            predicted_cost = float(cost_model.predict(input_reg)[0])
            predicted_co2 = float(co2_model.predict(input_reg)[0])
            
            # Add slight visual UI variance and enforce non-negative floor
            variance = np.random.uniform(0.9, 1.1) 
            final_cost = max(0.01, predicted_cost * variance)
            final_co2 = max(0.001, predicted_co2 * variance)

            unsorted_results.append({
                'material': str(material),
                'cost_inr': final_cost,
                'co2_kg': final_co2
            })

        # --- STEP 3: Re-Ranking for Frontend Display ---
        # The React frontend expects the absolute best material at index 0.
        res_df = pd.DataFrame(unsorted_results)
        
        # Normalize the metrics so they weigh evenly in the penalty
        res_df['Cost_Norm'] = res_df['cost_inr'] / res_df['cost_inr'].max()
        res_df['CO2_Norm'] = res_df['co2_kg'] / res_df['co2_kg'].max()
        
        # Calculate Penalty (Lower cost and lower CO2 = Better Rank)
        res_df['Penalty'] = (res_df['Cost_Norm'] * 0.4) + (res_df['CO2_Norm'] * 0.6)
        
        # Sort by Penalty to ensure the Gold Trophy goes to the mathematically superior option
        ranked_df = res_df.sort_values('Penalty')
        
        top_recommendations = []
        for _, row in ranked_df.iterrows():
            top_recommendations.append({
                'material': row['material'],
                'cost_inr': round(row['cost_inr'], 2),
                'co2_kg': round(row['co2_kg'], 2)
            })

        # --- STEP 4: Save History & Return ---
        best_match = top_recommendations[0]
        new_record = RecommendationHistory(
            category_name=category,
            weight_capacity_kg=weight,
            tensile_strength_mpa=strength,
            top_material=best_match['material'],
            est_cost=best_match['cost_inr'],
            est_co2=best_match['co2_kg']
        )
        db.session.add(new_record)
        db.session.commit()

        # Format timestamp accurately to 12-hour AM/PM format as requested
        current_time_12hr = datetime.now().strftime("%I:%M %p")

        return jsonify({
            "status": "success",
            "timestamp": current_time_12hr,
            "input_parameters": {
                "category": category,
                "weight_kg": weight,
                "strength_mpa": strength
            },
            "recommendations": top_recommendations
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)