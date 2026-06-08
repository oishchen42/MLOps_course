from sklearn.preprocessing import StandardScaler
import test_train_helpers as th
import pandas as pd
import dagster as dg

@dg.asset(
    group_name="machine_learning",
    description="Applies cyclical time encoding and scales features specifically for the linear model.",
    ins={"chronological_data_split": dg.AssetIn()}
)
def linear_model_preprocessing(chronological_data_split: dict) -> dict:
    """Prepares the chronological splits specifically for linear regression."""
    
    continuous_features = ['temperature_c', 'perceived_temperature_c', 'humidity', 
        'windspeed_kmh', 'conditions', 'rentals_24h_ago', 'rentals_7d_ago']

    return th.preprocess_train_test(
        chronological_data_split=chronological_data_split,
        apply_cyclical=True,
        features_to_scale=continuous_features
    )