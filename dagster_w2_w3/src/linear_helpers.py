import numpy as np
import pandas as pd

def apply_cyclical_time(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms linear hour and month into cyclical sine/cosine coordinates."""
    df_cyclic = df.copy()
    
    # Map hour (0-23) onto a 24-hour circle
    df_cyclic['hour_sin'] = np.sin(2 * np.pi * df_cyclic['hour'] / 24.0)
    df_cyclic['hour_cos'] = np.cos(2 * np.pi * df_cyclic['hour'] / 24.0)
    
    # Map month (1-12) onto a 12-month circle
    df_cyclic['month_sin'] = np.sin(2 * np.pi * df_cyclic['month'] / 12.0)
    df_cyclic['month_cos'] = np.cos(2 * np.pi * df_cyclic['month'] / 12.0)
    
    # Drop the original rigid columns so the linear model doesn't get confused
    df_cyclic = df_cyclic.drop(columns=['hour', 'month'])
    
    return df_cyclic