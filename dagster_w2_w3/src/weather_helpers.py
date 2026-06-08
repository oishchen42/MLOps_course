import pandas as pd

def map_conditions_from_one_to_four(df: pd.DataFrame) -> pd.DataFrame:
    """Map textual weather conditions to numeric codes 1-4.

    - Inputs: `df` with a `conditions` column containing textual labels
    - Output: DataFrame with `conditions` mapped to integers (1=clear ... 4=heavy_rain)
    """
    condition_mapping = {
        'clear': 1,
        'clouds': 2,
        'light_rain': 3,
        'heavy_rain': 4
    }
    print(df['conditions'].value_counts())
    df['conditions'] = df['conditions'].map(condition_mapping)
    return df