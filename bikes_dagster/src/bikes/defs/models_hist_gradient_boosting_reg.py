import dagster as dg
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

import model_helpers as mh

@dg.asset(
    name="advanced_tree_model",
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description="Trains a HistGradientBoostingRegressor on the engineered bike timeline.",
    ins={
        "dfs_united_with_time_features": dg.AssetIn()
    }
)
def advanced_tree_model(dfs_united_with_time_features: pd.DataFrame):
    """Trains a HistGradientBoostingRegressor on the engineered bike timeline.
    ------
    Value: The trained HistGradientBoostingRegressor model object.
    Metadata:
- RMSE: Root Mean Squared Error of the model on the test set.
- MAE: Mean Absolute Error of the model on the test set.
- R2_Score: R-squared score of the model on the test set.
- Feature_Importance: A markdown table showing the importance of each feature in the model.
------
return: A Dagster Output object containing the trained model and its evaluation metrics as metadata.
    """
    # Create a copy
    model_df = dfs_united_with_time_features.copy()
    
    # Convert the text string back into a mathematical datetime object
    model_df['datetime'] = pd.to_datetime(model_df['datetime'])
    
    # Convert boolean switches
    boolean_features = ['is_weekend', 'is_holiday'] 
    model_df[boolean_features] = model_df[boolean_features].astype(int)
    
    # Dismantle datetime
    model_df['hour'] = model_df['datetime'].dt.hour
    model_df['month'] = model_df['datetime'].dt.month
    
    # NO StandardScaler needed for the tree model, so we skip that

    columns_to_drop = ['datetime', 'direct_count', 'registered_count', 'total_rentals']
    X = model_df.drop(columns=columns_to_drop)
    y = model_df['total_rentals']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # 7. Train the mathematical model
    tree_model = HistGradientBoostingRegressor(max_iter=1000, random_state=42)
    tree_model.fit(X_train, y_train)
    
    # Evaluate the model
    predictions = tree_model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    #  Fetching Feature Importance
    importance_df = mh.analyze_feature_importance(tree_model, X_test, y_test)
    
    # Return the object AND the UI metadata
    # Value is just the tree_model since there is no scaler
    return dg.Output(
        value=tree_model,
        metadata={
            "RMSE": dg.MetadataValue.float(rmse),
            "MAE": dg.MetadataValue.float(mae),
            "R2_Score": dg.MetadataValue.float(r2),
            "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False))
        }
    )