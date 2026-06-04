import pandas as pd
import bikes_helpers
import holidays_helpers
import weather_helpers
import supply

def drop_id_convert_datetime(df: pd.DataFrame, datetime_col: str) -> pd.DataFrame:
    """Convert a column to datetime and drop id/date columns.

    - Inputs: `df`, `datetime_col` (name of column to parse as datetime)
    - Output: DataFrame with `datetime` column parsed and `id`/`date` removed if present
    """
    df["datetime"] = pd.to_datetime(df[datetime_col])
    df = df.drop(columns=['id', 'date'], errors='ignore')
    return df

def add_is_weekend(df: pd.DataFrame) -> pd.DataFrame:
    """Add an `is_weekend` boolean column.

    - Inputs: `df` with a `datetime` column
    - Output: DataFrame with `is_weekend` (True for Saturday/Sunday)
    """
    # Check if the numerical day of the week is 5 (Sat) or 6 (Sun)
    df['is_weekend'] = df["datetime"].dt.dayofweek >= 5
    return df