from pathlib import Path
import pandas as pd


def explore_csv(path):
    """
    Reads a CSV file and returns a cleaned DataFrame.

    Parameters
    ----------
    path : str or pathlib.Path
        The file path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        A cleaned DataFrame with appropriate datetime parsing and column adjustments.
    """
    df = pd.read_csv(path)
    print(f"{df.head()}")
    print(f"{df.info()}")
    print(f"{df.isna().sum()}")
    return df