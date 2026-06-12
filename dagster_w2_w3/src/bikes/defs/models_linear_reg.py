from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import dagster as dg
import pandas as pd
import model_helpers as mh
import mlflow
import os

@dg.asset(
    name="base_linear_model",
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description="Trains a base_linear_model on the engineered bike timeline.",
    ins={
        "linear_model_preprocessing": dg.AssetIn()
    }
)
def base_linear_model(linear_model_preprocessing: dict):
    """Train a linear regression on the engineered bike timeline.

    Parameters
    ----------
    dfs_united_with_time_features : pandas.DataFrame
        Engineered dataset containing feature columns and the target column `total_rentals`.

    Returns
    -------
    dagster.Output
        Dagster Output containing the trained model and fitted preprocessing objects; metadata includes
        evaluation metrics and a markdown table of feature importances.
    """
    # Unpack the preprocessed data
    X_train = linear_model_preprocessing["X_train"]
    X_test = linear_model_preprocessing["X_test"]
    y_train = linear_model_preprocessing["y_train"]
    y_test = linear_model_preprocessing["y_test"]
    scaler = linear_model_preprocessing["scaler"]
    
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    mlflow.set_tracking_uri(tracking_uri)

    mlflow.set_experiment("Bike Rentals Predictions")

    # Let MLflow capture all the model parameters and metrics automatically
    mlflow.sklearn.autolog()

    with mlflow.start_run(run_name="Linear Regression Run") as run:
        mlflow.set_tag("model_type", "Linear Regression")
        # Fit the linear model to the training data
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Generate predictions and compute performance metrics
        predictions = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R2_Score", r2)

        mlflow_run_url = f"http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}"

        # Calculate which features were most important for the model
        importance_df = mh.analyze_feature_importance(model, X_test, y_test)
        
        # Package the trained model and return detailed metrics
        return dg.Output(
            value=(model, scaler),
            metadata={
                "RMSE": dg.MetadataValue.float(rmse),
                "MAE": dg.MetadataValue.float(mae),
                "R2_Score": dg.MetadataValue.float(r2),
                "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False))
            }
        )