import pandas as pd

def engineer_time_features(df: pd.DataFrame):
    # 1. Create a working copy and ensure it is perfectly sorted by time
    # If the rows are out of order, the shift math will be entirely wrong.
    df_engineered = df.copy()
    df_engineered = df_engineered.sort_values('datetime').reset_index(drop=True)
    
    # 2. Lag Feature: Shift the answers down by exactly 24 rows (hours)
    df_engineered['rentals_24h_ago'] = df_engineered['total_rentals'].shift(24)
    
    # 3. Rolling Feature: Calculate the mean of the 3 strictly prior hours
    # .shift(1) ensures we don't accidentally include the CURRENT hour's rentals (which would be cheating)
    df_engineered['rolling_avg_3h'] = df_engineered['total_rentals'].shift(1).rolling(window=3).mean()
    
    # 4. Clean up the unavoidable NaNs
    # Shifting data down creates 24 blank rows at the very top of your dataset.
    df_engineered = df_engineered.dropna().reset_index(drop=True)
    
    return df_engineered