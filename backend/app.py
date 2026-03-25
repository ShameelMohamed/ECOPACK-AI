from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import joblib
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. Database Configuration (PostgreSQL)
# ==========================================
# IMPORTANT: Replace 'YOUR_PASSWORD_HERE' with your actual PostgreSQL password
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Infinity@localhost/ecopackai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Database Table Structure for BI Dashboards later
class RecommendationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    weight_capacity_kg = db.Column(db.Float, nullable=False)
    tensile_strength_mpa = db.Column(db.Float, nullable=False)
    top_material = db.Column(db.String(100), nullable=False)
    est_cost = db.Column(db.Float, nullable=False)
    est_co2 = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# ==========================================
# 2. Machine Learning Setup
# ==========================================
print("Loading ML Models...")
MODEL_DIR = '../model'
try:
    cost_model = joblib.load(os.path.join(MODEL_DIR, 'cost_model.pkl'))
    co2_model = joblib.load(os.path.join(MODEL_DIR, 'co2_model.pkl'))
except Exception as e:
    print(f"Error loading models: {e}. Make sure you run this from the 'backend' folder!")

AVAILABLE_MATERIALS = [
    'Recycled Plastic', 'Recycled Metal', 'Composite', 'Bioplastic', 
    'Biopolymer', 'Bio-Composite', 'Plant-Based', 'Natural Fiber', 
    'Agro-Waste Fiber', 'Recycled Fiber'
]

# ==========================================
# 3. REST API Endpoints
# ==========================================
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "database": "connected"})

@app.route('/api/recommend', methods=['POST'])
def recommend_packaging():
    try:
        # Parse JSON request from Frontend
        data = request.json
        category = data['category_name']
        weight = float(data['weight_capacity_kg'])
        strength = float(data['tensile_strength_mpa'])
        biodegradability = float(data.get('biodegradability_score', 50))
        recyclability = float(data.get('recyclability_percent', 50))

        results = []
        
        # Run the AI Simulation
        for material in AVAILABLE_MATERIALS:
            test_data = pd.DataFrame([{
                'category_name': category,
                'material_type': material,
                'tensile_strength_mpa': strength,
                'weight_capacity_kg': weight,
                'biodegradability_score': biodegradability,
                'recyclability_percent': recyclability
            }])
            
            predicted_cost = cost_model.predict(test_data)[0]
            predicted_co2 = co2_model.predict(test_data)[0]
            
            results.append({
                'material': material,
                'cost_inr': round(float(predicted_cost), 2),
                'co2_kg': round(float(predicted_co2), 2)
            })
            
        # Convert to DataFrame for Ranking
        results_df = pd.DataFrame(results)
        results_df['Cost_Rank'] = results_df['cost_inr'] / results_df['cost_inr'].max()
        results_df['CO2_Rank'] = results_df['co2_kg'] / results_df['co2_kg'].max()
        results_df['Penalty'] = (results_df['Cost_Rank'] * 0.5) + (results_df['CO2_Rank'] * 0.5)
        
        # Get Top 3 Recommendations
        ranked_df = results_df.sort_values(by='Penalty').head(3)
        top_recommendations = ranked_df[['material', 'cost_inr', 'co2_kg']].to_dict('records')

        # Save the best recommendation to PostgreSQL
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

        # Return JSON response
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "input_parameters": {
                "category": category,
                "weight_kg": weight,
                "strength_mpa": strength
            },
            "recommendations": top_recommendations
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)