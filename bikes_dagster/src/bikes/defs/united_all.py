import pandas as pd
import supply
import dagster as dg

import time_feature_engin_helpers as tf


@dg.asset(
    group_name="feature_engineered_data",
    io_manager_key="csv_export",
    ins={
        "merged_bikes_with_holidays": dg.AssetIn(),
        "weather": dg.AssetIn()
    }
)
def dfs_united_with_time_features(merged_bikes_with_holidays: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    """Produce feature-engineered dataset by merging rentals with weather and adding time features.

    Parameters
    ----------
    merged_bikes_with_holidays : pandas.DataFrame
        Bike rentals merged with holiday indicators.
    weather : pandas.DataFrame
        Weather observations indexed by `datetime`.

    Returns
    -------
    pandas.DataFrame
        Feature-engineered DataFrame with lag and rolling features added.
    """
    
    merged_bikes_with_holidays = merged_bikes_with_holidays.sort_values('datetime')
    weather = weather.sort_values('datetime')

    # how='left': This ensures every single hour from bike_df is preserved. If weather_df lacks a matching datetime,
    merged_df = pd.merge(merged_bikes_with_holidays, weather, on='datetime', how='left')

    # adding 2 new columns for modeling: renatls_24h_ago and rolling_avg_3h
    feature_engineered_df = tf.engineer_time_features(merged_df)

    return feature_engineered_df.reset_index(drop=True)