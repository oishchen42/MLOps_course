import numpy as np
import pandas as pd

def apply_cyclical_time(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms linear hour and month into cyclical sine/cosine coordinates."""
    df_cyclic = df.copy()
    
    # Convert hours to a circle: 0 and 23 are close together
    df_cyclic['hour_sin'] = np.sin(2 * np.pi * df_cyclic['hour'] / 24.0)
    df_cyclic['hour_cos'] = np.cos(2 * np.pi * df_cyclic['hour'] / 24.0)
    
    # Convert months to a circle: December and January are close together
    df_cyclic['month_sin'] = np.sin(2 * np.pi * df_cyclic['month'] / 12.0)
    df_cyclic['month_cos'] = np.cos(2 * np.pi * df_cyclic['month'] / 12.0)
    
    # Remove the original hour/month columns since we have the cyclical versions now
    df_cyclic = df_cyclic.drop(columns=['hour', 'month'])
    
    return df_cyclic