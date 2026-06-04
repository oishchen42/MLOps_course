import pandas as pd

def engineer_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df_engineered = df.copy()
    
    # Sort strictly by time to ensure shifts work correctly
    df_engineered = df_engineered.sort_values('datetime').reset_index(drop=True)
    
    # Create the lag and rolling memory features
    df_engineered['rentals_24h_ago'] = df_engineered['total_rentals'].shift(24)
    df_engineered['rolling_avg_3h'] = df_engineered['total_rentals'].shift(1).rolling(window=3).mean()
    
    # Drop the empty rows created by shifting
    df_engineered = df_engineered.dropna().reset_index(drop=True)
    
    return df_engineered