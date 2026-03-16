from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("ecopack_model.pkl", "rb"))

# Create FastAPI app
app = FastAPI()

# Input structure
class MaterialInput(BaseModel):
    strength: float
    weight_capacity: float
    biodegradability: float
    recyclability: float
    co2_emission: float


# Home route
@app.get("/")
def home():
    return {"message": "EcoPackAI API is running"}


# Prediction route
@app.post("/predict")
def predict_material(data: MaterialInput):

    input_data = np.array([[data.strength,
                            data.weight_capacity,
                            data.biodegradability,
                            data.recyclability,
                            data.co2_emission]])

    prediction = model.predict(input_data)

    return {
        "recommended_material": prediction[0]
    }
