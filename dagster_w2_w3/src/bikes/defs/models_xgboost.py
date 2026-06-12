import dagster as dg
import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

import model_helpers as mh 
import test_train_helpers as th
import os

@dg.asset(
    name="xgb_model",
    group_name="machine_learning",
    compute_kind="xgboost",
    description="Trains an XGBoost Regressor using 24h and 7d in mlflow",
    auto_materialize_policy=dg.AutoMaterializePolicy.eager(),
    ins={"chronological_data_split": dg.AssetIn()}
)
def xgb_model(chronological_data_split: dict):
    data = th.preprocess_train_test(
        chronological_data_split=chronological_data_split,
    )
    y_train = data["y_train"]
    X_train = data["X_train"]
    y_test = data["y_test"]
    X_test = data["X_test"]

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    mlflow.set_tracking_uri(tracking_uri)
    print(f"DEBUG: Using MLflow tracking URI: {tracking_uri}")

    mlflow.set_experiment("Bike Rentals Predictions")
    # mlflow.xgboost.autolog()
    with mlflow.start_run(run_name="XGBoost Run") as run:
        mlflow.set_tag("model_type", "XGBoost Regressor")
        xgb_model = xgb.XGBRegressor(n_estimators=1000, random_state=42, early_stopping_rounds=20)
        xgb_model.fit(
            X_train, 
            y_train,
            eval_set=[(X_test, y_test)],  # Let XGBoost evaluate performance on test data during training
            verbose=False  # Don't clutter the logs with training progress output
        )

        predictions = xgb_model.predict(X_test)
        rmse = root_mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        # Record the input/output schema so MLflow knows what data this model expects
        signature = mlflow.models.signature.infer_signature(X_train, predictions)

        mlflow.xgboost.log_model(
            xgb_model=xgb_model,
            artifact_path="model",
            signature=signature
        )

        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R2_Score", r2)

        importance_df = mh.analyze_feature_importance(xgb_model, X_test, y_test)
        mlflow_run_url = f"http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}"

        return dg.Output(
            value=xgb_model,
            metadata={
                "RMSE": dg.MetadataValue.float(rmse),
                "MAE": dg.MetadataValue.float(mae),
                "R2_Score": dg.MetadataValue.float(r2),
                "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False)),
                "MLflow_Run_URL": dg.MetadataValue.url(mlflow_run_url)
            }
        )