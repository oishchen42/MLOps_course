import pandas as pd
import supply
import dagster as dg

@dg.asset(
    group_name="bikes_merge",
    ins={
        "direct_pickup_bike_rentals": dg.AssetIn(),
        "registered_bike_rentals": dg.AssetIn()
    }
)
def united_bike_rentals(
    direct_pickup_bike_rentals: pd.DataFrame, 
    registered_bike_rentals: pd.DataFrame
) -> pd.DataFrame:
    """Merge direct and registered rentals into a single ledger and compute totals.

    Parameters
    ----------
    direct_pickup_bike_rentals : pandas.DataFrame
        Hourly aggregated direct pickup rentals with `direct_count`.
    registered_bike_rentals : pandas.DataFrame
        Hourly aggregated registered rentals with `registered_count`.

    Returns
    -------
    pandas.DataFrame
        Merged DataFrame with `direct_count`, `registered_count`, and `total_rentals`.
    """

    merged_df = pd.merge(
        direct_pickup_bike_rentals,
        registered_bike_rentals,
        on=['datetime', 'is_weekend'],
        how='outer'
    )

    # Fill missing values and compute the total
    merged_df['direct_count'] = merged_df['direct_count'].fillna(0)
    merged_df['registered_count'] = merged_df['registered_count'].fillna(0)
    merged_df['total_rentals'] = merged_df['direct_count'] + merged_df['registered_count']
    
    # Keep data in chronological order for time-series analysis
    merged_df = merged_df.sort_values('datetime').reset_index(drop=True)

    return merged_df