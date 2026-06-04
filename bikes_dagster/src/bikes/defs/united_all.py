import pandas as pd
import supply
import dagster as dg


@dg.asset(
    group_name="feature_engineered_data",
    io_manager_key="csv_export",
    ins={
        "merged_bikes_with_holidays": dg.AssetIn(),
        "weather": dg.AssetIn()
    }
)
def dfs_united(merged_bikes_with_holidays: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    # 1. Create matching date-only keys for both dataframes
    """Merges direct and registered bike rentals into a single master tracking dataset."""
    
    merged_bikes_with_holidays = merged_bikes_with_holidays.sort_values('datetime')
    weather = weather.sort_values('datetime')
    # how='left': This ensures every single hour from bike_df is preserved. If weather_df lacks a matching datetime,
    merged_df = pd.merge(merged_bikes_with_holidays, weather, on='datetime', how='left')
    
    return merged_df.reset_index(drop=True)