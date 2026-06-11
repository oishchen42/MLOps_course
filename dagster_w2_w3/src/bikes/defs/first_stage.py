import pandas as pd
import supply
import dagster as dg

import general_helpers as gh
import bikes_helpers as bh
import holidays_helpers as hh
import weather_helpers as wh

@dg.asset(
    group_name="initial_load",
    compute_kind="pandas",
    ins={"lakefs_raw_ingestion": dg.AssetIn()}
)
def direct_pickup_bike_rentals(lakefs_raw_ingestion: dict) -> pd.DataFrame:
    """Load direct pickup bike rentals and aggregate to hourly counts.

    Returns
    -------
    pandas.DataFrame
        Hourly aggregated direct pickup rentals with `direct_count` and `is_weekend`.
    """
    direct_uri = lakefs_raw_ingestion["direct_uri"]
    df = pd.read_csv(direct_uri)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = bh.aggregate_rentals_by_hour(df)
    df = gh.add_is_weekend(df)
    df = df.rename(columns={
        'rental_count': 'direct_count',
    })
    return df

@dg.asset(
    group_name="initial_load",
    compute_kind="pandas",
    ins={"lakefs_raw_ingestion": dg.AssetIn()}
)
def registered_bike_rentals(lakefs_raw_ingestion: dict) -> pd.DataFrame:
    """Load registered bike rentals and aggregate to hourly counts.

    Returns
    -------
    pandas.DataFrame
        Hourly aggregated registered rentals with `registered_count` and `is_weekend`.
    """
    registered_uri = lakefs_raw_ingestion["registered_uri"]
    df = pd.read_csv(registered_uri)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = bh.aggregate_rentals_by_hour(df)
    df = gh.add_is_weekend(df)
    df = df.rename(columns={
        'rental_count': 'registered_count',
    })
    return df

@dg.asset(
    group_name="initial_load",
    compute_kind="pandas",
    ins={"lakefs_raw_ingestion": dg.AssetIn()}
)
def holidays(lakefs_raw_ingestion: dict) -> pd.DataFrame:
    """Load holidays file and convert to holiday indicator format.

    Returns
    -------
    pandas.DataFrame
        Holidays DataFrame with `datetime` and `is_holiday` columns.
    """
    holidays_uri = lakefs_raw_ingestion["holidays_uri"]
    df = pd.read_csv(holidays_uri)
    df = gh.drop_id_convert_datetime(df, "date")
    df = hh.transform_to_holiday_indicator(df)
    return df

@dg.asset(
    group_name="initial_load",
    compute_kind="pandas",
    ins={"lakefs_raw_ingestion": dg.AssetIn()}
)
def weather(lakefs_raw_ingestion: dict) -> pd.DataFrame:
    """Load weather data and normalize condition codes.

    Returns
    -------
    pandas.DataFrame
        Weather DataFrame with normalized `conditions` and `datetime`.
    """
    weather_uri = lakefs_raw_ingestion["weather_uri"]
    df = pd.read_csv(weather_uri)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = wh.map_conditions_from_one_to_four(df)
    return df