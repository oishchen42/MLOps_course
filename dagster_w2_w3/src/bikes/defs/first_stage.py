import os
import pandas as pd
import dagster as dg
import lakefs_spec
import general_helpers as gh
import bikes_helpers as bh
import holidays_helpers as hh
import weather_helpers as wh

def get_lakefs_client():
    # The lakefs library looks for credentials in environment variables.
    # We set them here so the SDK can find them automatically.
    os.environ["LAKECTL_SERVER_ENDPOINT_URL"] = os.getenv("LAKECTL_SERVER_ENDPOINT_URL", "http://lakefs:8000")
    os.environ["LAKECTL_CREDENTIALS_ACCESS_KEY_ID"] = os.getenv("LAKECTL_CREDENTIALS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")
    os.environ["LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY"] = os.getenv("LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
    
    return lakefs_spec.LakeFSFileSystem()

@dg.asset(group_name="initial_load", compute_kind="pandas")
def direct_pickup_bike_rentals() -> pd.DataFrame:
    fs = get_lakefs_client()
    with fs.open("lakefs://bike-rentals/main/data/direct_pickup_bike_rentals.csv", "r") as f:
        df = pd.read_csv(f)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = bh.aggregate_rentals_by_hour(df)
    df = gh.add_is_weekend(df)
    df = df.rename(columns={'rental_count': 'direct_count'})
    return df

@dg.asset(group_name="initial_load", compute_kind="pandas")
def registered_bike_rentals() -> pd.DataFrame:
    fs = get_lakefs_client()
    with fs.open("lakefs://bike-rentals/main/data/registered_bike_rentals.csv", "r") as f:
        df = pd.read_csv(f)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = bh.aggregate_rentals_by_hour(df)
    df = gh.add_is_weekend(df)
    df = df.rename(columns={'rental_count': 'registered_count'})
    return df

@dg.asset(group_name="initial_load", compute_kind="pandas")
def holidays() -> pd.DataFrame:
    fs = get_lakefs_client()
    with fs.open("lakefs://bike-rentals/main/data/holidays.csv", "r") as f:
        df = pd.read_csv(f)
    df = gh.drop_id_convert_datetime(df, "date")
    df = hh.transform_to_holiday_indicator(df)
    return df

@dg.asset(group_name="initial_load", compute_kind="pandas")
def weather() -> pd.DataFrame:
    fs = get_lakefs_client()
    with fs.open("lakefs://bike-rentals/main/data/weather.csv", "r") as f:
        df = pd.read_csv(f)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = wh.map_conditions_from_one_to_four(df)
    return df