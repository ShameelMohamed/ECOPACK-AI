import joblib
import pandas as pd
import numpy as np

# 1. Load the tuned models
print("Loading tuned models...")
cost_model = joblib.load('cost_model.pkl')
co2_model = joblib.load('co2_model.pkl')

# 2. Extract feature names from the preprocessor
preprocessor = cost_model.named_steps['preprocessor']
num_features = ['tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'recyclability_percent']
cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(['category_name', 'material_type'])
all_features = np.concatenate([num_features, cat_features])

# 3. Analyze CO2 Model (XGBoost) Feature Importance
print("\n--- Top 5 Features for Predicting CO2 Emission ---")
co2_importances = co2_model.named_steps['regressor'].feature_importances_

# Pair features with their importance scores
co2_feature_importance = pd.DataFrame({
    'Feature': all_features,
    'Importance': co2_importances
}).sort_values(by='Importance', ascending=False)

print(co2_feature_importance.head(5).to_string(index=False))

# 4. Analyze Cost Model (Random Forest) Feature Importance
print("\n--- Top 5 Features for Predicting Cost ---")
cost_importances = cost_model.named_steps['regressor'].feature_importances_

cost_feature_importance = pd.DataFrame({
    'Feature': all_features,
    'Importance': cost_importances
}).sort_values(by='Importance', ascending=False)

print(cost_feature_importance.head(5).to_string(index=False))