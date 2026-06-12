from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import pandas as pd
import os

# 1. Corrected Schema based on MLflow Signature
class BikeRentalInput(BaseModel):
    is_weekend: int
    is_holiday: int
    conditions: int
    temperature_c: float
    perceived_temperature_c: float
    humidity: float
    windspeed_kmh: float
    hour: int
    month: int

app = FastAPI(title="Bike Rentals Prediction API")

tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(tracking_uri)

model_name = "Bike_Rentals_Predictor"
alias = "champion"
model_uri = f"models:/{model_name}@{alias}"

try:
    model = mlflow.pyfunc.load_model(model_uri)
    print(f"Successfully loaded model: {model_uri}")
except Exception as e:
    print(f"Warning: Model not found. Train the model via Dagster first. Error: {e}")
    model = None

@app.post("/predict")
def predict(data: BikeRentalInput):
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model is not yet trained and loaded. Please run the Dagster pipeline first."
        )

    # Convert incoming JSON payload into a Pandas DataFrame
    input_df = pd.DataFrame([data.model_dump()])
    
    # Inject exact dummy lag features the model expects
    input_df["rentals_24h_ago"] = 0.0
    input_df["rentals_7d_ago"] = 0.0
    
    # Generate the prediction
    prediction = model.predict(input_df)
    
    return {
        "predicted_rentals": float(prediction[0])
    }