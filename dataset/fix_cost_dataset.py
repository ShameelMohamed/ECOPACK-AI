import pandas as pd
import numpy as np

# 1. Load the dataset (We use the one we just fixed for CO2!)
print("Loading engineered dataset...")
df = pd.read_csv('engineered_ecopack_dataset.csv')

# 2. Define realistic base costs per kg (in INR) for each material
# Eco-friendly materials like Bioplastics usually have a higher market price
base_cost_per_kg = {
    'Recycled Plastic': 40,
    'Recycled Metal': 80,
    'Composite': 70,
    'Bioplastic': 120,      
    'Biopolymer': 150,
    'Bio-Composite': 130,
    'Plant-Based': 90,
    'Natural Fiber': 60,
    'Agro-Waste Fiber': 50,
    'Recycled Fiber': 45
}

# 3. Calculate base material cost (Weight * Base Price)
df['Material_Cost_INR'] = df['weight_capacity_kg'] * df['material_type'].map(base_cost_per_kg)

# 4. Add engineering premiums
# High tensile strength requires advanced manufacturing (+0.5 INR per MPa)
df['Material_Cost_INR'] += df['tensile_strength_mpa'] * 0.5

# High biodegradability score carries an eco-premium (+2.0 INR per score point)
df['Material_Cost_INR'] += df['biodegradability_score'] * 2.0

# 5. Add realistic market fluctuation (random noise)
np.random.seed(42)
# Adds a random fluctuation to simulate real-world price changes
df['Material_Cost_INR'] += np.random.normal(0, 150, len(df)) 

# 6. Save the fully engineered dataset
output_name = 'final_engineered_dataset.csv'
df.to_csv(output_name, index=False)
print(f"Economics fixed! Dataset saved as: {output_name}")