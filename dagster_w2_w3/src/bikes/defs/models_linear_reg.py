from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import dagster as dg
import pandas as pd
import model_helpers as mh
import mlflow

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
    # Create a copy
    X_train = linear_model_preprocessing["X_train"]
    X_test = linear_model_preprocessing["X_test"]
    y_train = linear_model_preprocessing["y_train"]
    y_test = linear_model_preprocessing["y_test"]
    scaler = linear_model_preprocessing["scaler"]
    
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("Bike Rentals Predictions")

    mlflow.sklearn.autolog()  # Automatically logs parameters, metrics, and the model itself

    with mlflow.start_run(run_name="Linear Regression Run") as run:
        mlflow.set_tag("model_type", "Linear Regression")
        # 2. Train the mathematical model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # 3. Evaluate the model
        predictions = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R2_Score", r2)

        mlflow_run_url = f"http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}"

        # 4. Fetch Feature Importance (Assuming mh.analyze_feature_importance exists)
        importance_df = mh.analyze_feature_importance(model, X_test, y_test)
        
        # 5. Return the objects and log metadata to the UI
        return dg.Output(
            value=(model, scaler),
            metadata={
                "RMSE": dg.MetadataValue.float(rmse),
                "MAE": dg.MetadataValue.float(mae),
                "R2_Score": dg.MetadataValue.float(r2),
                "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False))
            }
        )