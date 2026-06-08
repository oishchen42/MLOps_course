from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
import dagster as dg
import model_helpers as mh 
import pandas as pd
import test_train_helpers as th

@dg.asset(
    name="advanced_xgboost_model",
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description="Trains an HistGradientBoosting Regressor using 24h and 7d memory features.",
    ins={"chronological_data_split": dg.AssetIn()}
)
def advanced_xgboost_model(chronological_data_split: dict):
    # 1. Unpack the split data directly
    data = th.preprocess_train_test(
        chronological_data_split=chronological_data_split,)
    
    y_train = data["y_train"]
    X_train = data["X_train"]
    
    y_test = data["y_test"]
    X_test = data["X_test"]
    
    # 3. Train the HistGradientBoosting Model
    # n_estimators=1000 replaces the max_iter parameter from the previous model
    xgb_model = HistGradientBoostingRegressor(max_iter=1000, random_state=42)
    xgb_model.fit(X_train, y_train)
    
    # 4. Evaluate the model
    predictions = xgb_model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # 5. Fetch Feature Importance
    importance_df = mh.analyze_feature_importance(xgb_model, X_test, y_test)
    
    # 6. Return the object and log metadata to the UI
    return dg.Output(
        value=xgb_model,
        metadata={
            "RMSE": dg.MetadataValue.float(rmse),
            "MAE": dg.MetadataValue.float(mae),
            "R2_Score": dg.MetadataValue.float(r2),
            "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False))
        }
    )