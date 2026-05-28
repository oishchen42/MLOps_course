import pandas as pd
from . import supply
import dagster as dg


@dg.asset(group_name="raw_data")
def direct_pickup_bike_rentals() -> pd.DataFrame:
    """
    Ingests raw direct pickups, formats time, flags the source, and drops indexes.
    
    Parameters
    ----------
    None
    Returns
    -------
    pandas.DataFrame
        A *cleaned* dataframe containing direct pickup bike rental information with a datetime index and an 'is_registered' flag set to False.
    """
    df = pd.read_csv(supply.PATH_DIRECT_PICKUP_BIKE)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df['is_registered'] = False
    df = df.drop(columns=['id'])
    return df

@dg.asset(group_name="raw_data")
def holidays() -> pd.DataFrame:
    """
    Ingests and cleans the holidays data.

    Parameters
    ----------
    None
    Returns
    -------
    pandas.DataFrame
        A *cleaned* dataframe containing holiday information with a datetime index.
    """
    df = pd.read_csv(supply.PATH_HOLIDAYS)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['is_holiday'] = True
    df = df.drop(columns=['id'])
    return df

@dg.asset(group_name="raw_data")
def registered_bike_rentals() -> pd.DataFrame:
    """
    Ingests and cleans the registered bike rentals data.

    Parameters
    ----------
    None
    Returns
    -------
    pandas.DataFrame
        A *cleaned* dataframe containing registered bike rental information with a datetime index."""
    df = pd.read_csv(supply.PATH_REGISTERED_BIKE)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df = df.drop(columns=['id'])
    df['is_registered'] = True
    return df

@dg.asset(group_name="raw_data")
def weather() -> pd.DataFrame:
    """
    Ingests and cleans the weather data.

    Parameters
    ----------
    None
    Returns
    -------
    pandas.DataFrame
        A *cleaned* dataframe containing weather information with a datetime index.
    """
    df = pd.read_csv(supply.PATH_WEATHER)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.drop(columns=['id'])
    return df

@dg.asset(group_name="processed_data")
def merge_regdir_bikes(registered_bike_rentals, direct_pickup_bike_rentals):
    """
    Stacks the registered and direct rental tables vertically into a single ledger.

    Parameters
    ----------
    registered_bike_rentals : pandas.DataFrame
        The *cleaned* dataframe of registered bike rentals.
    direct_pickup_bike_rentals : pandas.DataFrame
        The *cleaned* dataframe of direct pickup bike rentals.
    
    """
    master_bikes = pd.concat([registered_bike_rentals, direct_pickup_bike_rentals], ignore_index=True)
    return master_bikes

def align_time(merge_regdir_bikes):
    """
    HELEPER FUNCTION:Creates perfectly aligned time keys for merging without destroying the precise datetime.

    Parameters
    ----------
    merge_regdir_bikes : pandas.DataFrame
        The master dataframe containing both registered and direct bike rentals.

    Returns
    -------
    pandas.DataFrame
        A new dataframe with appended 'join_hour' and 'join_date' columns for temporal merging.
    """
    # We rename the internal variable to match the incoming asset
    master_df = merge_regdir_bikes.copy() 
    master_df['join_hour'] = master_df['datetime'].dt.floor('h')
    master_df['join_date'] = pd.to_datetime(master_df['datetime'].dt.date)
    return master_df

def engineer_time_features(df):
    """
    HELEPER FUNCTION:Extracts standalone numerical features from the exact timestamp.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the 'datetime' column to be engineered.
    Returns
    -------
    pandas.DataFrame
        A new dataframe with additional time-based features extracted from the 'datetime' column.
    """
    engineered_df = df.copy()
    
    # Extract the hour (0-23)
    # Why: Bike rentals heavily depend on morning/evening rush hours.
    engineered_df['hour'] = engineered_df['datetime'].dt.hour
    
    # Extract the day of the week (Monday=0, Sunday=6)
    # Why: Commuters rent on weekdays; tourists rent on weekends.
    engineered_df['day_of_week'] = engineered_df['datetime'].dt.dayofweek
    
    return engineered_df

def encode_weather_conditions(df):
    """
    HELEPER FUNCTION:Simplifies and encodes weather conditions into machine-readable features.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the 'conditions' column to be encoded.
    Returns
    -------
    pandas.DataFrame
        A new dataframe with the 'conditions' column replaced by booleans-like encoded weather features.
    """
    engineered_df = df.copy()
    engineered_df['conditions'] = engineered_df['conditions'].replace(
        ['heavy_rain', 'light_rain'], 
        'rain'
    )
    
    # Encoding: Explode the text column into independent boolean columns
    # prefix='weather' ensures ther new columns are neatly named (e.g., 'weather_clear')
    # dtype=bool ensures we get True/False instead of 1/0, matching is_holiday column
    engineered_df = pd.get_dummies(
        engineered_df, 
        columns=['conditions'], 
        prefix='weather',
        dtype=bool
    )
    
    return engineered_df

@dg.asset(group_name="final_data")
def feature_engineered_dataset(merge_regdir_bikes, weather, holidays):
    """
    Performs Left Joins to attach weather and holiday context.

    Parameters
    ----------
    merge_regdir_bikes : pandas.DataFrame
        The master dataframe containing both registered and direct bike rentals
    weather : pandas.DataFrame
        The dataframe containing weather information
    holidays : pandas.DataFrame
        The dataframe containing holiday information
    Returns
    -------
    pandas.DataFrame
        A fully feature-engineered dataframe ready for modeling, with weather and holiday context merged in.
    """
    aligned_df = align_time(merge_regdir_bikes)  # Get the aligned dataframe with join keys
    # Merge Weather on the hourly key (using the incoming 'align_time' asset)
    merged_df = pd.merge(
        aligned_df, 
        weather, 
        left_on='join_hour', 
        right_on='datetime', 
        how='left',
        suffixes=('', '_weather')
    )
    
    # Merge Holidays on the daily key (using the incoming 'holidays' asset)
    merged_df = pd.merge(
        merged_df,
        holidays,
        left_on='join_date',
        right_on='date',
        how='left'
    )
    
    # Cleanup Nan
    merged_df['is_holiday'] = merged_df['is_holiday'].fillna(False).astype(bool)
    
    # Drop the redundant merge keys
    columns_to_drop = ['join_hour', 'join_date', 'datetime_weather', 'date']
    merged_df = merged_df.drop(columns=columns_to_drop)
    merged_df = encode_weather_conditions(merged_df)  # Apply weather encoding to the merged dataframe
    merged_df = engineer_time_features(merged_df)  # Apply time feature engineering to the merged dataframe
    with open("feature_engineered_bike_rentals.csv", "w") as f:
        f.write(merged_df.to_csv(index=False))  
    return merged_df

# *cleaned* meanse that the id column has been dropped, datetime is in datetime format, and the is_registered flag is set.