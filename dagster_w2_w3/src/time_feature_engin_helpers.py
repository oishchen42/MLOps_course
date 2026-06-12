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

    # Time-series shifts only work correctly when data is sorted chronologically
    df_engineered = df_engineered.sort_values('datetime').reset_index(drop=True)

    # Extract temporal features and create lagged features
    df_engineered['datetime'] = pd.to_datetime(df_engineered['datetime'])
    df_engineered['hour'] = df_engineered['datetime'].dt.hour
    df_engineered['month'] = df_engineered['datetime'].dt.month
    df_engineered['rentals_24h_ago'] = df_engineered['total_rentals'].shift(24)
    df_engineered['target_7d_ago'] = df_engineered['datetime'] - pd.Timedelta(days=7)

    history_df = df_engineered[['datetime', 'total_rentals']].copy()
    history_df = history_df.rename(columns={'total_rentals': 'rentals_7d_ago'})

    # Find historical values from 7 days ago by joining on approximate datetime match
    df_engineered = pd.merge_asof(
        left=df_engineered,
        right=history_df,
        left_on='target_7d_ago',
        right_on='datetime',
        direction='backward',
        suffixes=('', '_drop')
    )
    
    # Remove temporary columns and drop rows with missing values from lagging
    df_engineered = df_engineered.drop(columns=['target_7d_ago', 'datetime_drop'])
    df_engineered = df_engineered.dropna().reset_index(drop=True)

    return df_engineered