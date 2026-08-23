import os
import pandas as pd

def ensure_dir(directory):
    """
    Ensures that a directory exists. If not, creates it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_csv_safe(filepath):
    """
    Safely reads a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=["date"])
        return df
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return pd.DataFrame()
