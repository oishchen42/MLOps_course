import pandas as pd

def map_conditions_from_one_to_four(df: pd.DataFrame) -> pd.DataFrame:
    condition_mapping = {
        'clear': 1,
        'clouds': 2,
        'light_rain': 3,
        'heavy_rain': 4
    }
    df['conditions'] = df['conditions'].map(condition_mapping)
    return df