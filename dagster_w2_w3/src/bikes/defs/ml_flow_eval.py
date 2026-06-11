import dagster as dg
import mlflow
from mlflow.tracking import MlflowClient

@dg.asset(
    name="champion_challenger_evaluator",
    group_name="machine_learning",
    compute_kind="mlflow",
    description="Evaluates recent MLflow runs and assigns champion/challenger aliases based on RMSE",
    ins={
        "xgb_model": dg.AssetIn(),
        "base_linear_model": dg.AssetIn(),
        "hist_gradient_boosting_model": dg.AssetIn()
    }
)
def champion_challenger_evaluator(context: dg.AssetExecutionContext, xgb_model, hist_gradient_boosting_model, base_linear_model):
    """Evaluates recent MLflow runs and assigns aliases based on RMSE performance."""
    
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    client = MlflowClient()
    model_name = "Bike_Rentals_Predictor"
    experiment_name = "Bike Rentals Predictions"
    
    # 1. Initialize the Registry
    try:
        client.create_registered_model(model_name)
    except Exception:
        pass # Proceeds if the registry already exists
        
    # 2. Fetch the two most recent model runs
    experiment = client.get_experiment_by_name(experiment_name)
    recent_runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=2
    )
    
    # 3. Retrieve the current champion's score
    try:
        champion_version = client.get_model_version_by_alias(model_name, "champion")
        champion_run = client.get_run(champion_version.run_id)
        current_champion_rmse = champion_run.data.metrics["RMSE"]
    except Exception:
        # If no champion exists (first run), set an infinitely high baseline
        current_champion_rmse = float('inf')
        
    # 4. Execute the comparison logic
    for run in recent_runs:
        new_rmse = run.data.metrics.get("RMSE", float('inf'))
        
        # Register the physical model into the MLflow Registry
        run_uri = f"runs:/{run.info.run_id}/model"
        model_version = mlflow.register_model(model_uri=run_uri, name=model_name)
        
        # 5. Assign aliases based on the outcome
        if new_rmse < current_champion_rmse:
            client.set_registered_model_alias(model_name, "champion", model_version.version)
            current_champion_rmse = new_rmse # Update the baseline so the next model must beat this new score
            context.log.info(f"Champion promoted: Run {run.info.run_id} (RMSE: {new_rmse})")
        else:
            client.set_registered_model_alias(model_name, "challenger", model_version.version)
            context.log.info(f"Challenger assigned: Run {run.info.run_id} (RMSE: {new_rmse})")

    return dg.Output(value="Evaluation Complete")