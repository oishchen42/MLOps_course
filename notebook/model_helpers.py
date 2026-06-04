from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.inspection import permutation_importance
import pandas as pd

# 1. Prepare the DataFrame
def linear_model_pipeline(df_united: pd.DataFrame) -> None:
    model_df = df_united.copy()

    # Convert boolean switches
    boolean_features = ['is_weekend', 'is_holiday'] 
    model_df[boolean_features] = model_df[boolean_features].astype(int)

    # Dismantle datetime
    model_df['hour'] = model_df['datetime'].dt.hour
    model_df['month'] = model_df['datetime'].dt.month

    # Scale continuous features
    continuous_features = ['hour', 'month', 'temperature_c', 'humidity', 'windspeed_kmh', 'conditions', 'perceived_temperature_c', 'rentals_24h_ago', 'rolling_avg_3h']
    scaler = StandardScaler()
    model_df[continuous_features] = scaler.fit_transform(model_df[continuous_features])

    # 2. Define X (features) and y (target)
    columns_to_drop = ['datetime', 'direct_count', 'registered_count', 'total_rentals']
    X = model_df.drop(columns=columns_to_drop)
    y = model_df['total_rentals']

    # 3. Split chronologically
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 4. Train the mathematical baseline
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    # 5. Evaluate the model
    predictions = linear_model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("=== Full Linear Model Evaluation ===")
    print(f"RMSE: {rmse:.2f} bikes")
    print(f"MAE:  {mae:.2f} bikes")
    print(f"R²:   {r2:.2f}")

    # 6. Extract Feature Importance
    print("\nScrambling columns to calculate exact feature reliance...")
    result = permutation_importance(
        linear_model, 
        X_test, 
        y_test, 
        scoring='neg_root_mean_squared_error', 
        n_repeats=10, 
        random_state=42
    )

    importance_df = pd.DataFrame({
        'Feature': X_test.columns,
        'Importance_Score': result.importances_mean
    }).sort_values(by='Importance_Score', ascending=False).reset_index(drop=True)

    print("\n=== Feature Importance Ranking ===")
    print(importance_df)