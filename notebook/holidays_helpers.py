import pandas as pd

def transform_to_holiday_indicator(df: pd.DataFrame) -> pd.DataFrame:
    df['is_holiday'] = True
    df = df.drop(columns=["holiday"])
    return df