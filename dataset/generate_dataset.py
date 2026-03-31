import pandas as pd
import numpy as np

# Set seed for reproducible results
np.random.seed(42)
n_rows = 10000

# 1. Product mapping (Industry -> Product Name, Min Weight, Max Weight)
industries = {
    'Healthcare': [('Sterile Injection Syringe', 0.01, 0.1), ('Specimen Collection Container', 0.05, 0.5), ('Surgical Tray', 0.2, 2.0)],
    'Automotive': [('Engine Bracket', 50, 250), ('Dashboard Panel', 2, 15), ('Bumper Core', 10, 50)],
    'Cosmetics': [('High-Gloss Skincare Tube', 0.05, 0.3), ('Compact Powder Case', 0.05, 0.2), ('Lotion Pump Bottle', 0.1, 0.5)],
    'Electronics': [('Laptop Chassis', 1.0, 3.5), ('Smartphone Casing', 0.1, 0.3), ('PCB Support Frame', 0.05, 0.5)],
    'Food & Beverage': [('Takeaway Container', 0.1, 1.0), ('Beverage Bottle', 0.2, 2.0), ('Bulk Grain Sack', 10, 50)],
    'Construction': [('Exterior Cladding Panel', 20, 150), ('Insulation Board', 5, 30), ('Support Beam', 100, 800)],
    'E-commerce': [('Shipping Box', 0.5, 25), ('Protective Mailer', 0.1, 5), ('Cushioning Insert', 0.05, 2)],
    'Agriculture': [('Seedling Tray', 0.1, 5), ('Fertilizer Drum', 10, 100), ('Irrigation Pipe', 5, 50)],
    'Home Appliances': [('Thermal Insulation Insert', 1, 10), ('Motor Support Frame', 5, 40), ('Refrigerator Liner', 2, 15)],
    'Toys': [('Action Figure Shell', 0.1, 1), ('Building Block Set', 0.5, 5), ('Ride-on Car Chassis', 10, 40)]
}

# 2. Strict Mathematical Bounds for each Material (Per KG)
# This completely prevents the model from getting biased or confusing materials.
material_bounds = {
    'Recycled Metal':   {'tensile': (300, 900), 'bio': (0, 5),   'recy': (80, 100), 'co2_per_kg': (5.0, 10.0), 'cost_per_kg': (50, 150)},
    'Composite':        {'tensile': (200, 700), 'bio': (5, 15),  'recy': (10, 30),  'co2_per_kg': (4.0, 8.0),  'cost_per_kg': (80, 200)},
    'Bio-Composite':    {'tensile': (60, 200),  'bio': (30, 60), 'recy': (30, 60),  'co2_per_kg': (2.0, 5.0),  'cost_per_kg': (40, 100)},
    'Recycled Plastic': {'tensile': (30, 90),   'bio': (5, 15),  'recy': (70, 95),  'co2_per_kg': (2.0, 4.0),  'cost_per_kg': (15, 40)},
    'Bioplastic':       {'tensile': (20, 60),   'bio': (50, 85), 'recy': (40, 70),  'co2_per_kg': (1.5, 3.5),  'cost_per_kg': (25, 80)},
    'Biopolymer':       {'tensile': (15, 50),   'bio': (60, 95), 'recy': (30, 70),  'co2_per_kg': (1.0, 3.0),  'cost_per_kg': (30, 90)},
    'Plant-Based':      {'tensile': (5, 30),    'bio': (70, 100),'recy': (20, 50),  'co2_per_kg': (0.5, 2.0),  'cost_per_kg': (5, 25)},
    'Natural Fiber':    {'tensile': (10, 40),   'bio': (80, 100),'recy': (20, 60),  'co2_per_kg': (0.5, 2.0),  'cost_per_kg': (5, 30)},
    'Agro-Waste Fiber': {'tensile': (1, 25),    'bio': (80, 100),'recy': (20, 50),  'co2_per_kg': (0.1, 1.5),  'cost_per_kg': (2, 15)},
    'Recycled Fiber':   {'tensile': (5, 35),    'bio': (40, 80), 'recy': (50, 90),  'co2_per_kg': (1.0, 2.5),  'cost_per_kg': (5, 20)}
}

data = []
categories = list(industries.keys())
materials = list(material_bounds.keys())

for _ in range(n_rows):
    # Select random category and product
    cat = np.random.choice(categories)
    prod_tuple = industries[cat][np.random.randint(0, len(industries[cat]))]
    prod_name = prod_tuple[0]
    min_w, max_w = prod_tuple[1], prod_tuple[2]
    
    # Select random material
    mat = np.random.choice(materials)
    b = material_bounds[mat]
    
    # Generate Physics limits cleanly inside the bounds
    weight = round(np.random.uniform(min_w, max_w), 3)
    tensile = round(np.random.uniform(b['tensile'][0], b['tensile'][1]), 2)
    bio = round(np.random.uniform(b['bio'][0], b['bio'][1]), 1)
    recy = round(np.random.uniform(b['recy'][0], b['recy'][1]), 1)
    
    # CRITICAL FIX: Cost and CO2 are strictly tied to the weight capacity of the product.
    # This prevents the XGBoost model from failing or flatlining.
    co2 = round(np.random.uniform(b['co2_per_kg'][0], b['co2_per_kg'][1]) * weight, 3)
    cost = round(np.random.uniform(b['cost_per_kg'][0], b['cost_per_kg'][1]) * weight, 2)
    
    data.append([f"{mat} {prod_name}", cat, mat, tensile, weight, bio, co2, recy, cost])

columns = ['Product', 'category_name', 'material_type', 'tensile_strength_mpa', 'weight_capacity_kg', 'biodegradability_score', 'co2_emission_kg_per_kg', 'recyclability_percent', 'Material_Cost_INR']
df = pd.DataFrame(data, columns=columns)

import os
os.makedirs('dataset', exist_ok=True)
df.to_csv('dataset/cleaned_ecopack_dataset yp.csv', index=False)
print("Successfully generated 10,000 perfectly bounded rows.")