import pandas as pd
import supply

def aggregate_rentals_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate event rows into hourly rental counts.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with a `datetime` column.

    Returns
    -------
    pandas.DataFrame
        DataFrame with `datetime` floored to the hour and `rental_count`.
    """
    df['datetime'] = df['datetime'].dt.floor('h')
    aggregated_df = df.groupby(['datetime']).size().reset_index(name='rental_count')
    return aggregated_df