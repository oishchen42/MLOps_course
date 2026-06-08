# import dagster as dg
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import HistGradientBoostingRegressor
# from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

# import model_helpers as mh

# @dg.asset(
#     name="advanced_tree_model",
#     group_name="machine_learning",
#     compute_kind="scikit-learn",
#     description="Trains a HistGradientBoostingRegressor on the engineered bike timeline.",
#     ins={
#         "dfs_united_with_time_features": dg.AssetIn()
#     }
# )
# def advanced_tree_model(dfs_united_with_time_features: pd.DataFrame):
#     """Train a histogram-based gradient boosting regressor on the engineered bike timeline.

#     Parameters
#     ----------
#     dfs_united_with_time_features : pandas.DataFrame
#         Engineered dataset containing feature columns and the target column `total_rentals`.

#     Returns
#     -------
#     dagster.Output
#         Dagster Output containing the trained model; metadata includes evaluation metrics and
#         a markdown table of feature importances.
#     """
#     # Create a copy
#     model_df = dfs_united_with_time_features.copy()
    
#     # NO StandardScaler needed for the tree model, so we skip that

#     columns_to_drop = ['datetime', 'direct_count', 'registered_count', 'total_rentals']
#     X = model_df.drop(columns=columns_to_drop)
#     y = model_df['total_rentals']

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
#     # Train the mathematical model
#     tree_model = HistGradientBoostingRegressor(max_iter=1000, random_state=42)
#     tree_model.fit(X_train, y_train)
    
#     # Evaluate the model
#     predictions = tree_model.predict(X_test)
#     rmse = root_mean_squared_error(y_test, predictions)
#     mae = mean_absolute_error(y_test, predictions)
#     r2 = r2_score(y_test, predictions)
    
#     #  Fetching Feature Importance
#     importance_df = mh.analyze_feature_importance(tree_model, X_test, y_test)
    
#     # Return the object AND the UI metadata
#     # Value is just the tree_model since there is no scaler
#     return dg.Output(
#         value=tree_model,
#         metadata={
#             "RMSE": dg.MetadataValue.float(rmse),
#             "MAE": dg.MetadataValue.float(mae),
#             "R2_Score": dg.MetadataValue.float(r2),
#             "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False))
#         }
#     )