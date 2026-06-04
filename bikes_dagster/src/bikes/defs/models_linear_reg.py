from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import dagster as dg
import pandas as pd
import model_helpers as mh

@dg.asset(
    name="base_linear_model",
    group_name="machine_learning",
    compute_kind="scikit-learn",
    description="Trains a base_linear_model on the engineered bike timeline.",
    ins={
        "dfs_united_with_time_features": dg.AssetIn()
    }
)
def base_linear_model(dfs_united_with_time_features: pd.DataFrame):
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
    
    # Scaling continuous features (as linear models are sensitive to feature scales)
    continuous_features = ['hour', 'month', 'temperature_c', 'humidity', 'windspeed_kmh', 'conditions', 'perceived_temperature_c']
    scaler = StandardScaler()
    model_df[continuous_features] = scaler.fit_transform(model_df[continuous_features])

    columns_to_drop = ['datetime', 'direct_count', 'registered_count', 'total_rentals']
    X = model_df.drop(columns=columns_to_drop)
    y = model_df['total_rentals']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Training the mathematical model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluating the model
    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    #  Fetching Feature Importance (Fixed bug: 'model' instead of 'tree_model')
    importance_df = mh.analyze_feature_importance(model, X_test, y_test)
    
    return dg.Output(
        value=(model, scaler),
        metadata={
            "RMSE": dg.MetadataValue.float(rmse),
            "MAE": dg.MetadataValue.float(mae),
            "R2_Score": dg.MetadataValue.float(r2),
            "Feature_Importance": dg.MetadataValue.md(importance_df.to_markdown(index=False))
        }
    )