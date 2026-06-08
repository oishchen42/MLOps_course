import pandas as pd

def engineer_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create lag and rolling features for hourly rentals.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing `datetime` and `total_rentals` columns.

    Returns
    -------
    pandas.DataFrame
        DataFrame with `rentals_24h_ago` and `rentals_7d_ago` added; rows with NaNs dropped.
    """
    df_engineered = df.copy()

    # Sort strictly by time to ensure shifts work correctly
    df_engineered = df_engineered.sort_values('datetime').reset_index(drop=True)

    # Create the lag and rolling memory features
    df_engineered['datetime'] = pd.to_datetime(df_engineered['datetime'])
    df_engineered['hour'] = df_engineered['datetime'].dt.hour
    df_engineered['month'] = df_engineered['datetime'].dt.month
    df_engineered['rentals_24h_ago'] = df_engineered['total_rentals'].shift(24)
    df_engineered['target_7d_ago'] = df_engineered['datetime'] - pd.Timedelta(days=7)

    history_df = df_engineered[['datetime', 'total_rentals']].copy()
    history_df = history_df.rename(columns={'total_rentals': 'rentals_7d_ago'})

    # Drop the empty rows created by shifting
    df_engineered = pd.merge_asof(
        left=df_engineered,
        right=history_df,
        left_on='target_7d_ago',
        right_on='datetime',
        direction='backward',
        suffixes=('', '_drop')
    )
    
    # 5. Clean up the temporary math columns and drop the initial rows with NaNs
    df_engineered = df_engineered.drop(columns=['target_7d_ago', 'datetime_drop'])
    df_engineered = df_engineered.dropna().reset_index(drop=True)

    return df_engineered