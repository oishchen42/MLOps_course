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

    # Extract just the date (without time) from both dataframes to match on
    united_bike_rentals['date_key'] = united_bike_rentals['datetime'].dt.date
    holidays['date_key'] = holidays['datetime'].dt.date

    holiday_subset = holidays[['date_key', 'is_holiday']]
    # Join holiday info to rentals, keeping all rental records even if holiday info is missing
    merged_df = pd.merge(united_bike_rentals, holiday_subset, on='date_key', how='left')

    # Fill missing values (non-holiday days) with 0
    merged_df['is_holiday'] = merged_df['is_holiday'].fillna(0).astype(int)

    # Remove the temporary date key since we don't need it anymore
    merged_df = merged_df.drop(columns=['date_key'])

    return merged_df