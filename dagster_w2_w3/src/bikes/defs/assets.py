import pandas as pd
from . import supply
import dagster as dg

def raw_store_events(path) -> pd.DataFrame:
    """Loads store events and aligns the timestamp column."""
    # Reads the file and immediately renames 'event_day' to 'datetime'
    df = pd.read_csv(path)
    df = df.rename(columns={"date": "datetime"})
    return df

def clean_basic(df):
    clean_df = df.copy()
    clean_df['datetime'] = pd.to_datetime(clean_df['datetime'], errors='coerce')
    return clean_df.drop(columns=["id"], errors='ignore')

def prepare_bikes(raw_df, event_type_name):
    engineered_df = raw_df.copy()
    # 1. Floor the time down to the hour
    engineered_df["floor_datetime"] = engineered_df["datetime"].dt.floor("h")
    
    # 2. Group by the floored time and count the rows
    summary_df = engineered_df.groupby("floor_datetime").size().reset_index(name="rents_per_hour")
    
    # 3. Add the identifying flag to the summarized data
    summary_df["is_registered"] = event_type_name
    
    return summary_df

def prepare_holidays(raw_df):
    final_df = raw_df.copy()
    return final_df.assign(is_holiday=True).drop(columns=["holiday_name"])

def prepare_weather(df):
    # Directly explodes the categorical column without grouping prior values
    encoded_df = df.copy()
    encoded_df = pd.get_dummies(
        df, 
        columns=['conditions'], 
        prefix='weather_', 
        dtype=bool
    )
    return encoded_df

def merge_bikes(registered_df, direct_df):
    merged_df = pd.concat([registered_df, direct_df], ignore_index=True)
    return merged_df


def merge_weather_holidays(weather_cleaned_df, holidays_cleaned_df):
    weather_df = weather_cleaned_df.copy()
    holidays_df = holidays_cleaned_df.copy()
    
    # Create daily key for merging
    weather_df['join_date'] = weather_df['datetime'].dt.normalize()
    
    # Merge Weather on the hourly key
    merged_df = pd.merge(
        left=weather_df,
        right=holidays_df,
        how='left',
        left_on='join_date',
        right_on='datetime'
    )
    
    # Cleanup Nan
    merged_df['is_holiday'] = merged_df['is_holiday'].fillna(False).astype(bool)
    
    # Resolve Pandas Suffix Collision: 
    # Drop the temporary join date and the holiday's original datetime ('datetime_y')
    merged_df = merged_df.drop(columns=['join_date', 'datetime_y'])
    
    # Rename the weather's original datetime ('datetime_x') to match the bike ledger
    merged_df = merged_df.rename(columns={'datetime_x': 'floor_datetime'})
    
    return merged_df

@dg.asset(group_name="raw_data")
def holliday() -> pd.DataFrame:
    return raw_store_events(supply.PATH_HOLIDAYS)

@dg.asset(group_name="raw_data")
def weather() -> pd.DataFrame:
    return raw_store_events(supply.PATH_WEATHER)

@dg.asset(group_name="raw_data")
def registered_bike_rentals() -> pd.DataFrame:
    return raw_store_events(supply.PATH_REGISTERED_BIKE)

@dg.asset(group_name="raw_data")
def direct_pickup_bike_rentals() -> pd.DataFrame:
    return raw_store_events(supply.PATH_DIRECT_PICKUP_BIKE)

@dg.asset(group_name="cleaned_data")
def cleaned_holidays(holliday) -> pd.DataFrame:
    return clean_basic(holliday)

@dg.asset(group_name="cleaned_data")
def cleaned_weather(weather) -> pd.DataFrame:
    return clean_basic(weather)

@dg.asset(group_name="cleaned_data")
def cleaned_registered_bike_rentals(registered_bike_rentals) -> pd.DataFrame:
    return clean_basic(registered_bike_rentals)

@dg.asset(group_name="cleaned_data")
def cleaned_direct_pickup_bike_rentals(direct_pickup_bike_rentals) -> pd.DataFrame:
    df = clean_basic(direct_pickup_bike_rentals)
    return df

@dg.asset(group_name="merge_preparation")
def registered_merge_ready(cleaned_registered_bike_rentals) -> pd.DataFrame:
    return prepare_bikes(cleaned_registered_bike_rentals, True)

@dg.asset(group_name="merge_preparation")
def direct_merge_ready(cleaned_direct_pickup_bike_rentals) -> pd.DataFrame:
    return prepare_bikes(cleaned_direct_pickup_bike_rentals, False)

@dg.asset(group_name="merge_preparation")
def holidays_merge_ready(cleaned_holidays) -> pd.DataFrame:
    return prepare_holidays(cleaned_holidays)

@dg.asset(group_name="final_part")
def weather_merge_ready(cleaned_weather) -> pd.DataFrame:
    return prepare_weather(cleaned_weather)

@dg.asset(group_name="final_part")
def merge_regdir_bikes(registered_merge_ready, direct_merge_ready):
    return merge_bikes(registered_merge_ready, direct_merge_ready)

@dg.asset(group_name="result")
def model_ready_dataset(merge_regdir_bikes, weather_merge_ready) -> pd.DataFrame:
    final_df = pd.merge(
        left=merge_regdir_bikes,
        right=weather_merge_ready,
        how='left',
        on='floor_datetime' # Both tables now share this exact column name
    )
    
    # Persist the final output as per acceptance criteria
    # final_df.to_csv("feature_engineered_bike_rentals.csv", index=False)
    
    return final_df

