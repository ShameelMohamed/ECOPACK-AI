import pandas as pd
import joblib

# 1. Load the trained and tuned AI models
print("Loading AI Models for Recommendation Engine...")
cost_model = joblib.load('cost_model.pkl')
co2_model = joblib.load('co2_model.pkl')

# Define all available packaging materials in the system
AVAILABLE_MATERIALS = [
    'Recycled Plastic', 'Recycled Metal', 'Composite', 'Bioplastic', 
    'Biopolymer', 'Bio-Composite', 'Plant-Based', 'Natural Fiber', 
    'Agro-Waste Fiber', 'Recycled Fiber'
]

def get_best_packaging(category, weight_capacity, tensile_strength, min_biodegradability, min_recyclability):
    """
    Simulates all materials for the given product constraints and ranks them.
    """
    results = []
    
    # 2. Test every material against the product requirements
    for material in AVAILABLE_MATERIALS:
        # Create a test profile for this specific material
        test_data = pd.DataFrame([{
            'category_name': category,
            'material_type': material,
            'tensile_strength_mpa': tensile_strength,
            'weight_capacity_kg': weight_capacity,
            'biodegradability_score': min_biodegradability,
            'recyclability_percent': min_recyclability
        }])
        
        # Predict Cost and CO2
        predicted_cost = cost_model.predict(test_data)[0]
        predicted_co2 = co2_model.predict(test_data)[0]
        
        results.append({
            'Material': material,
            'Estimated_Cost_INR': round(predicted_cost, 2),
            'Estimated_CO2_kg': round(predicted_co2, 2)
        })
        
    # Convert results to a DataFrame for easy ranking
    results_df = pd.DataFrame(results)
    
    # 3. Define the Ranking Algorithm
    # We want low Cost and low CO2. We normalize both columns so they can be added together equally.
    results_df['Cost_Rank_Score'] = results_df['Estimated_Cost_INR'] / results_df['Estimated_Cost_INR'].max()
    results_df['CO2_Rank_Score'] = results_df['Estimated_CO2_kg'] / results_df['Estimated_CO2_kg'].max()
    
    # Combined Penalty Score (Lower is better). 
    # You can change the weights here! (e.g., 0.7 for CO2 if the company prioritizes the environment over cost)
    results_df['Total_Penalty_Score'] = (results_df['Cost_Rank_Score'] * 0.5) + (results_df['CO2_Rank_Score'] * 0.5)
    
    # Sort by the lowest penalty score
    ranked_recommendations = results_df.sort_values(by='Total_Penalty_Score').reset_index(drop=True)
    
    # Return the top 3 recommendations
    return ranked_recommendations[['Material', 'Estimated_Cost_INR', 'Estimated_CO2_kg']].head(3)

# ==========================================
# 4. Test the Engine!
# ==========================================
if __name__ == "__main__":
    print("\n--- Running AI Packaging Simulation ---")
    print("Product: Heavy Duty Healthcare Equipment")
    print("Constraints: 800kg capacity, 400 MPa strength\n")
    
    top_3 = get_best_packaging(
        category='Healthcare',
        weight_capacity=800,
        tensile_strength=400,
        min_biodegradability=60,
        min_recyclability=80
    )
    
    print("🏆 Top 3 Recommended Materials:")
    print(top_3.to_string(index=False))