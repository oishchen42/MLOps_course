from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import pandas as pd
import os

class BikeRentalInput(BaseModel):
    is_weekend: int
    direct_count: float
    registered_count: float
    is_holiday: int
    conditions: float
    temperature_c: float
    perceived_temperature_c: float
    humidity: float
    windspeed_kmh: float

app = FastAPI(title="Bike Rentals Prediction API")

tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
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
    # Make sure we have a trained model before trying to make predictions.
    # If someone hits this endpoint before running the pipeline, we need to let them know.
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model is not yet trained and loaded. Please run the Dagster pipeline first."
        )

    input_df = pd.DataFrame([data.model_dump()])
    prediction = model.predict(input_df)
    
    return {
        "predicted_rentals": float(prediction[0])
    }