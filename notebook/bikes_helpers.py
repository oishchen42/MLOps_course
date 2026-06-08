import pandas as pd
import supply

def aggregate_rentals_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    df['datetime'] = df['datetime'].dt.floor('h')
    aggregated_df = df.groupby(['datetime']).size().reset_index(name='rental_count')
    return aggregated_df