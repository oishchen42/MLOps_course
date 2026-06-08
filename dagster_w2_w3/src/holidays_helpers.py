import pandas as pd

def transform_to_holiday_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """Mark all rows as holidays and normalize schema.

    - Inputs: `df` containing holiday rows
    - Output: DataFrame with `is_holiday` column set to True and `holiday` column removed
    """
    df['is_holiday'] = 1
    df = df.drop(columns=["holiday"])
    return df