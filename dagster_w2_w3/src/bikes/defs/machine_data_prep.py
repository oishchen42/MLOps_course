import pandas as pd
import dagster as dg

@dg.asset(
    group_name="models_data_preparation",
    description="Slices the engineered data chronologically (80/20) into train and test sets.",
    ins={"dfs_united_with_time_features": dg.AssetIn()}
)
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