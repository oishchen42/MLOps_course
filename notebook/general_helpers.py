import pandas as pd
import bikes_helpers
import holidays_helpers
import weather_helpers
import supply

def drop_id_convert_datetime(df: pd.DataFrame, datetime_col: str) -> pd.DataFrame:
    df["datetime"] = pd.to_datetime(df[datetime_col])
    # if "date" in df.columns:
    #     df = df.drop(columns=['date'])
    df = df.drop(columns=['id', 'date'], errors='ignore')
    return df

def add_is_weekend(df: pd.DataFrame) -> pd.DataFrame:
    # Check if the numerical day of the week is 5 (Sat) or 6 (Sun)
    df['is_weekend'] = df["datetime"].dt.dayofweek >= 5
    return df