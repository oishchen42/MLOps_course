from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import pandas as pd
import os

# 1. Define the exact input schema your model expects
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

# 2. Tell the API where the MLflow server is located

# Dynamically fetch the URI from Docker, or fallback to localhost if running outside Docker
tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(tracking_uri)

# 3. Load the model dynamically from the registry into memory when the server starts
model_uri = "models:/Bike_Rentals_Champion@production"
model = mlflow.pyfunc.load_model(model_uri)

# 4. Expose the prediction endpoint
@app.post("/predict")
def predict(data: BikeRentalInput):
    # Convert the incoming JSON payload into a Pandas DataFrame
    input_df = pd.DataFrame([data.model_dump()])
    
    # Generate the prediction
    prediction = model.predict(input_df)
    
    return {
        "predicted_rentals": float(prediction[0])
    }