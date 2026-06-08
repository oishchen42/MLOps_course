import pandas as pd
import supply
import general_helpers as gh
import bikes_helpers as bh
import os
from pathlib import Path

def registered_bike_rentals() -> pd.DataFrame:
    """Load registered bike rentals and aggregate to hourly counts.

    Returns
    -------
    pandas.DataFrame
        Hourly aggregated registered rentals with `registered_count` and `is_weekend`.
    """
    df = pd.read_csv(supply.PATH_REGISTERED_BIKE)
    df = gh.drop_id_convert_datetime(df, "datetime")
    df = bh.aggregate_rentals_by_hour(df)
    df = gh.add_is_weekend(df)
    df = df.rename(columns={
        'rental_count': 'registered_count',
    })
    return df

def chronological_data_split(dfs_united_with_time_features: pd.DataFrame) -> dict:
    """
    Returns a dictionary containing the Train and Test DataFrames.
    """
    df = dfs_united_with_time_features.copy()
    
    # Calculate the exact row index for the 80% cutoff
    split_index = int(len(df) * 0.8)
    
    # Slice the data chronologically
    train_df = df.iloc[:split_index].reset_index(drop=True)
    test_df = df.iloc[split_index:].reset_index(drop=True)

    # Return as a dictionary so downstream models can easily access them
    return {
        "train": train_df,
        "test": test_df
    }

def main():
    df_test = registered_bike_rentals()
    dic = chronological_data_split(df_test)
    print("Train DataFrame:")
    print(dic["train"].head())
    print("\nTest DataFrame:")
    print(dic["test"].head())
    # target_path = Path("/Users/OleksiiIshchenko/mlops_course/mlops/data/")
    # print(os.listdir(target_path))

main()