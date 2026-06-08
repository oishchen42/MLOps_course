import pandas as pd
import supply
import dagster as dg

@dg.asset(
    group_name="merge_bikes_holidays",
    ins={
        "united_bike_rentals": dg.AssetIn(),
        "holidays": dg.AssetIn()
    }
)
def merged_bikes_with_holidays(united_bike_rentals: pd.DataFrame, holidays: pd.DataFrame) -> pd.DataFrame:
    """Merge bike rentals with holiday indicators on date.

    Parameters
    ----------
    united_bike_rentals : pandas.DataFrame
        DataFrame of hourly bike rental aggregates containing `datetime`.
    holidays : pandas.DataFrame
        Holidays DataFrame containing `datetime` and `is_holiday`.

    Returns
    -------
    pandas.DataFrame
        Merged DataFrame with an `is_holiday` boolean column.
    """

    # 1. Create matching date-only keys for both dataframes
    united_bike_rentals['date_key'] = united_bike_rentals['datetime'].dt.date
    holidays['date_key'] = holidays['datetime'].dt.date

    holiday_subset = holidays[['date_key', 'is_holiday']]
    # 3. Perform a left join using our normalized date key
    merged_df = pd.merge(united_bike_rentals, holiday_subset, on='date_key', how='left')

    # 4. Fill the unfulfilled NaN spaces with False
    merged_df['is_holiday'] = merged_df['is_holiday'].fillna(0).astype(int)

    # 5. Drop the temporary key so it doesn't clutter our final output
    merged_df = merged_df.drop(columns=['date_key'])

    return merged_df