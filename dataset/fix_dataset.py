import pandas as pd
import numpy as np

# 1. Load the original dataset
print("Loading original dataset...")
df = pd.read_csv('cleaned_ecopack_dataset yp.csv')

# 2. Define realistic baseline CO2 emissions for each material type
material_co2 = {
    'Recycled Plastic': 4.5,
    'Recycled Metal': 6.0,
    'Composite': 5.0,
    'Bioplastic': 2.5,
    'Biopolymer': 2.0,
    'Bio-Composite': 3.0,
    'Plant-Based': 1.0,
    'Natural Fiber': 1.2,
    'Agro-Waste Fiber': 0.8,
    'Recycled Fiber': 1.5
}

# 3. Apply the base CO2 logic based on the material
df['co2_emission_kg_per_kg'] = df['material_type'].map(material_co2)

# 4. Add a relationship for Tensile Strength (Stronger/denser material requires more energy)
df['co2_emission_kg_per_kg'] += df['tensile_strength_mpa'] * 0.005

# 5. Add a small amount of random noise (to make it a realistic AI problem, not just a perfect formula)
np.random.seed(42)
df['co2_emission_kg_per_kg'] += np.random.normal(0, 0.2, len(df))

# 6. Save the new, logically sound dataset
output_name = 'engineered_ecopack_dataset.csv'
df.to_csv(output_name, index=False)
print(f"Dataset successfully fixed and saved as: {output_name}")