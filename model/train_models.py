import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

os.makedirs('model', exist_ok=True)
os.makedirs('dataset', exist_ok=True)

# ==========================================
# 1. Dataset Generation
# ==========================================
print("1. Generating 10,000 rows with Industry & Physics Logic...")
np.random.seed(42)
n_rows = 10000

industries = {
    'Healthcare':      (0.01, 2.0,  1.40, 1.25),
    'Automotive':      (2.0, 250.0, 1.15, 1.20),
    'Cosmetics':       (0.05, 0.5,  1.35, 1.10),
    'Electronics':     (0.05, 5.0,  1.25, 1.05),
    'Food & Beverage': (0.1, 2.0,   0.85, 0.90),
    'Construction':    (5.0, 800.0, 0.75, 1.15),
    'E-commerce':      (0.1, 25.0,  0.80, 0.85),
    'Agriculture':     (0.1, 100.0, 0.65, 0.85),
    'Home Appliances': (2.0, 40.0,  1.05, 1.10),
    'Toys':            (0.1, 10.0,  0.90, 0.95)
}

material_bounds = {
    'Recycled Metal':   {'tensile': (300, 900), 'bio': (0, 5),   'recy': (80, 100), 'co2': 8.0, 'cost': 100},
    'Composite':        {'tensile': (200, 700), 'bio': (5, 15),  'recy': (10, 30),  'co2': 6.0, 'cost': 150},
    'Bio-Composite':    {'tensile': (60, 200),  'bio': (30, 60), 'recy': (30, 60),  'co2': 3.5, 'cost': 70},
    'Recycled Plastic': {'tensile': (30, 90),   'bio': (5, 15),  'recy': (70, 95),  'co2': 3.0, 'cost': 30},
    'Bioplastic':       {'tensile': (20, 60),   'bio': (50, 85), 'recy': (40, 70),  'co2': 2.5, 'cost': 50},
    'Biopolymer':       {'tensile': (15, 50),   'bio': (60, 95), 'recy': (30, 70),  'co2': 2.0, 'cost': 60},
    'Plant-Based':      {'tensile': (5, 30),    'bio': (70, 100),'recy': (20, 50),  'co2': 1.0, 'cost': 15},
    'Natural Fiber':    {'tensile': (10, 40),   'bio': (80, 100),'recy': (20, 60),  'co2': 1.2, 'cost': 20},
    'Agro-Waste Fiber': {'tensile': (1, 25),    'bio': (80, 100),'recy': (20, 50),  'co2': 0.5, 'cost': 10},
    'Recycled Fiber':   {'tensile': (5, 35),    'bio': (40, 80), 'recy': (50, 90),  'co2': 1.5, 'cost': 12}
}

data = []
categories = list(industries.keys())
materials = list(material_bounds.keys())

for _ in range(n_rows):
    cat = np.random.choice(categories)
    min_w, max_w, cost_mult, co2_mult = industries[cat]
    
    mat = np.random.choice(materials)
    b = material_bounds[mat]
    
    weight = np.random.uniform(min_w, max_w)
    tensile = np.random.uniform(b['tensile'][0], b['tensile'][1])
    bio = np.random.uniform(b['bio'][0], b['bio'][1])
    recy = np.random.uniform(b['recy'][0], b['recy'][1])
    
    base_cost = weight * b['cost'] * cost_mult
    base_co2 = weight * b['co2'] * co2_mult
    
    noise_cost = np.random.normal(1.0, 0.05) 
    noise_co2 = np.random.normal(1.0, 0.05)
    
    final_cost = max(0.01, base_cost * noise_cost)
    final_co2 = max(0.001, base_co2 * noise_co2)
    
    data.append([f"Generic {mat} Item", cat, mat, tensile, weight, bio, final_co2, recy, final_cost])

df = pd.DataFrame(data, columns=['Product', 'category_name', 'material_type', 'tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'co2_emission_kg_per_kg', 'recyclability_percent', 'Material_Cost_INR'])
df.to_csv('dataset/cleaned_ecopack_dataset yp.csv', index=False)


# ==========================================
# 2. Feature Engineering & Encoders
# ==========================================
clf_features = ['category_name', 'tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'recyclability_percent']
reg_features = ['category_name', 'material_type', 'tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'recyclability_percent']

X_clf = df[clf_features].copy()
X_reg = df[reg_features].copy()

encoders = {}
cat_le = LabelEncoder()
X_clf['category_name'] = cat_le.fit_transform(X_clf['category_name'])
X_reg['category_name'] = cat_le.transform(X_reg['category_name'])
encoders['category_name'] = cat_le

mat_le = LabelEncoder()
y_material = mat_le.fit_transform(df['material_type'])
X_reg['material_type'] = y_material
encoders['material_type'] = mat_le

joblib.dump(encoders, 'model/categorical_encoders.pkl')

y_cost = df['Material_Cost_INR']
y_co2 = df['co2_emission_kg_per_kg']

X_clf_train, X_clf_test, y_mat_train, y_mat_test = train_test_split(X_clf, y_material, test_size=0.2, random_state=42)
X_reg_train, X_reg_test, y_cost_train, y_cost_test, y_co2_train, y_co2_test = train_test_split(X_reg, y_cost, y_co2, test_size=0.2, random_state=42)

# ==========================================
# 3. Model Training
# ==========================================
print("\n2. Training Model 1: Material Classifier (XGBoost Gatekeeper)...")
xgb_classifier = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42, n_jobs=-1)
xgb_classifier.fit(X_clf_train, y_mat_train)

print("3. Training Model 2: Cost Predictor (Random Forest)...")
cost_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
cost_model.fit(X_reg_train, y_cost_train)

print("4. Training Model 3: CO2 Estimator (XGBoost)...")
co2_model = XGBRegressor(n_estimators=150, max_depth=6, learning_rate=0.08, random_state=42, n_jobs=-1)
co2_model.fit(X_reg_train, y_co2_train)

# ==========================================
# 4. Evaluation
# ==========================================
print("\n--- Material Classifier Evaluation ---")
mat_preds = xgb_classifier.predict(X_clf_test)
print(f"Accuracy : {accuracy_score(y_mat_test, mat_preds) * 100:.2f}% (Physics Engine Check)")

def evaluate_model(name, model, X_t, y_t):
    predictions = model.predict(X_t)
    r2 = r2_score(y_t, predictions)
    rmse = np.sqrt(mean_squared_error(y_t, predictions))
    print(f"\n--- {name} Evaluation ---")
    print(f"R² Score : {r2:.4f} (Target: 0.90 to 0.98)")
    print(f"RMSE     : {rmse:.4f}")

evaluate_model("Cost Predictor (Random Forest)", cost_model, X_reg_test, y_cost_test)
evaluate_model("CO2 Estimator (XGBoost)", co2_model, X_reg_test, y_co2_test)

joblib.dump(xgb_classifier, 'model/xgb_classifier.pkl')
joblib.dump(cost_model, 'model/cost_predictor_rf.pkl')
joblib.dump(co2_model, 'model/co2_estimator_xgb.pkl')
print("\nSuccess! All 3 Models saved.")

# ==========================================
# 5. VALIDATION: Real-World Physics Check
# ==========================================
print("\n==========================================")
print("SYSTEM VALIDATION (With Physics Gatekeeper)")
print("==========================================")

user_inputs = [
    {"name": "Heavy Engine Part", "cat": "Automotive", "str": 500.0, "wt": 150.0, "bio": 2.0, "recy": 95.0},
    {"name": "E-Commerce Box", "cat": "E-commerce", "str": 40.0, "wt": 5.0, "bio": 60.0, "recy": 85.0},
    {"name": "Sterile Medical Tray", "cat": "Healthcare", "str": 30.0, "wt": 0.5, "bio": 80.0, "recy": 40.0},
    {"name": "Delicate Cosmetic Jar", "cat": "Cosmetics", "str": 25.0, "wt": 0.1, "bio": 90.0, "recy": 70.0},
    {"name": "Steel Construction Beam", "cat": "Construction", "str": 700.0, "wt": 600.0, "bio": 5.0, "recy": 90.0}
]

# FIX: Extract the Encoders here before the loop!
cat_encoder = encoders['category_name']
mat_encoder = encoders['material_type']

for user_data in user_inputs:
    print(f"\n[Scenario: {user_data['name']}]")
    print(f"Inputs -> Industry: {user_data['cat']} | Load: {user_data['wt']}kg | Str: {user_data['str']}MPa | Bio: {user_data['bio']} | Recy: {user_data['recy']}")
    
    encoded_cat = cat_encoder.transform([user_data['cat']])[0]
    
    # STEP 1: Classifier filters for Physics!
    input_clf = pd.DataFrame([[
        encoded_cat, user_data['str'], user_data['wt'], user_data['bio'], user_data['recy']
    ]], columns=clf_features)
    
    probs = xgb_classifier.predict_proba(input_clf)[0]
    top_3_idx = np.argsort(probs)[::-1][:3]
    top_3_mats = mat_encoder.inverse_transform(top_3_idx)
    
    print("Top 3 Physically Viable Materials:")
    
    # STEP 2: Regressors price only the Top 3
    for i, mat in enumerate(top_3_mats):
        encoded_mat = mat_encoder.transform([mat])[0]
        
        input_reg = pd.DataFrame([[
            encoded_cat, encoded_mat, user_data['str'], user_data['wt'], user_data['bio'], user_data['recy']
        ]], columns=reg_features)
        
        # Base predictions + UI Variance
        variance = np.random.uniform(0.9, 1.1)
        predicted_cost = max(0.01, float(cost_model.predict(input_reg)[0]) * variance)
        predicted_co2 = max(0.001, float(co2_model.predict(input_reg)[0]) * variance)
        
        print(f"  # {mat:<18} | Est Cost: ₹ {predicted_cost:<8.2f} | Est CO2: {predicted_co2:.4f} kg")