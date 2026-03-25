import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# 1. Load the dataset
print("Loading dataset...")
df = pd.read_csv('../dataset/final_engineered_dataset.csv')

# 2. Define Features (Inputs) and Targets (Outputs)
X = df[['category_name', 'material_type', 'tensile_strength_mpa', 'weight_capacity_kg', 
        'biodegradability_score', 'recyclability_percent']]

y_cost = df['Material_Cost_INR']
y_co2 = df['co2_emission_kg_per_kg']

# 3. Create a Preprocessing Pipeline
numeric_features = ['tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'recyclability_percent']
categorical_features = ['category_name', 'material_type']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# 4. Split data into 80% training and 20% testing
X_train_cost, X_test_cost, y_train_cost, y_test_cost = train_test_split(X, y_cost, test_size=0.2, random_state=42)
X_train_co2, X_test_co2, y_train_co2, y_test_co2 = train_test_split(X, y_co2, test_size=0.2, random_state=42)

# ---------------------------------------------------------
# 5. Tune and Train the Cost Prediction Model (Random Forest)
# ---------------------------------------------------------
print("\nTuning and Training Cost Prediction Model (Random Forest)...")
cost_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                ('regressor', RandomForestRegressor(random_state=42))])

# Define the hyperparameter grid for Random Forest
cost_param_grid = {
    'regressor__n_estimators': [50, 100, 150],      # Number of trees
    'regressor__max_depth': [None, 10, 20],         # Maximum depth of the tree
    'regressor__min_samples_split': [2, 5]          # Minimum samples required to split an internal node
}

# Run Grid Search
cost_grid_search = GridSearchCV(cost_pipeline, cost_param_grid, cv=5, scoring='r2', n_jobs=-1)
cost_grid_search.fit(X_train_cost, y_train_cost)

# Get the best model and test it
best_cost_model = cost_grid_search.best_estimator_
cost_preds = best_cost_model.predict(X_test_cost)

print("--- Tuned Cost Prediction Results ---")
print(f"Best Settings: {cost_grid_search.best_params_}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test_cost, cost_preds)):.2f}")
print(f"MAE: {mean_absolute_error(y_test_cost, cost_preds):.2f}")
print(f"R² Score: {r2_score(y_test_cost, cost_preds):.4f}")

# ---------------------------------------------------------
# 6. Tune and Train the CO2 Emission Model (XGBoost)
# ---------------------------------------------------------
print("\nTuning and Training CO2 Emission Model (XGBoost)...")
co2_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', XGBRegressor(random_state=42))])

# Define the hyperparameter grid for XGBoost
co2_param_grid = {
    'regressor__n_estimators': [50, 100, 200],      # Number of trees
    'regressor__max_depth': [3, 5, 7],              # Maximum depth of each tree
    'regressor__learning_rate': [0.01, 0.1, 0.2]    # Learning speed
}

# Run Grid Search
co2_grid_search = GridSearchCV(co2_pipeline, co2_param_grid, cv=5, scoring='r2', n_jobs=-1)
co2_grid_search.fit(X_train_co2, y_train_co2)

# Get the best model and test it
best_co2_model = co2_grid_search.best_estimator_
co2_preds = best_co2_model.predict(X_test_co2)

print("--- Tuned CO2 Emission Results ---")
print(f"Best Settings: {co2_grid_search.best_params_}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test_co2, co2_preds)):.2f}")
print(f"MAE: {mean_absolute_error(y_test_co2, co2_preds):.2f}")
print(f"R² Score: {r2_score(y_test_co2, co2_preds):.4f}")

# ---------------------------------------------------------
# 7. Save the best models
# ---------------------------------------------------------
print("\nSaving best models to disk...")
joblib.dump(best_cost_model, 'cost_model.pkl')
joblib.dump(best_co2_model, 'co2_model.pkl')
print("Done! Both models are successfully rebuilt and fine-tuned.")