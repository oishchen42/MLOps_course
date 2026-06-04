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
    """Merges direct and registered bike rentals into a single master tracking dataset."""

    merged_df = pd.merge(
        direct_pickup_bike_rentals,
        registered_bike_rentals,
        on=['datetime', 'is_weekend'],
        how='outer'
    )

    # Clean and sum
    merged_df['direct_count'] = merged_df['direct_count'].fillna(0)
    merged_df['registered_count'] = merged_df['registered_count'].fillna(0)
    merged_df['total_rentals'] = merged_df['direct_count'] + merged_df['registered_count']
    
    # Sort chronologically to make downstream EDA and modeling easier
    merged_df = merged_df.sort_values('datetime').reset_index(drop=True)

    return merged_df