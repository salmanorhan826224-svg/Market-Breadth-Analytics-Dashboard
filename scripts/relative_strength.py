import os
import glob
import pandas as pd
import requests
from datetime import date, timedelta
from tqdm import tqdm

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from config.config import API_KEY
POLYGON_DATA_DIR = "polygon_stock_data"
RS_OUTPUT_FILE = "output/rs_values_output_with_sectors.xlsx"

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

def calculate_relative_strength(stock_closes, ref_closes, period=14):
    """Computes the relative strength value."""
    if len(stock_closes) < period or len(ref_closes) < period:
        return None

    ratio = stock_closes / ref_closes
    delta = ratio.diff().dropna()

    gains = delta.apply(lambda x: x if x > 0 else 0)
    losses = delta.apply(lambda x: -x if x < 0 else 0)

    avg_gain = gains[-period:].mean()
    avg_loss = losses[-period:].mean()

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_stock_sector(api_key, ticker):
    """Fetches the sector information of a given stock."""
    url = f"https://api.polygon.io/v3/reference/tickers/{ticker}"
    params = {'apiKey': api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Warning: Failed to fetch sector for {ticker}.")
        return "Unknown"

    data = response.json()
    return data.get('results', {}).get('sector', "Unknown")
import pandas as pd

def compute_html_table_from_excel(file_path):
    """
    Reads an Excel file and converts it to an HTML table.
    
    Args:
        file_path (str): Path to the Excel file.
    
    Returns:
        str: HTML table as a string, or an empty string if an error occurs.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Convert the DataFrame to an HTML table
        html_table = df.to_html(index=False, classes='data-table', border=0)
        
        return html_table
    except Exception as e:
        print(f"Error reading or converting Excel file: {e}")
        return ""
def calculate_relative_strengths(api_key, polygon_data_dir, output_excel, qqq_df, period=14):
    """Computes RS values for stocks and saves the top 20 with sectors to an Excel file."""
    
    # Ensure QQQ Data index is datetime and normalized
    if not isinstance(qqq_df.index, pd.DatetimeIndex):
        qqq_df.index = pd.to_datetime(qqq_df.index)
    qqq_df.index = qqq_df.index.normalize()
    
    qqq_closes = qqq_df['close'].dropna()
    file_list = [f for f in glob.glob(os.path.join(polygon_data_dir, "*.csv")) if os.path.getsize(f) >= 10_000]
    rs_values = []
    # print(f"QQQ Data Date Range: {qqq_df.index.min()} to {qqq_df.index.max()}")


    for filepath in tqdm(file_list, desc="Processing stock data", unit="file"):
        ticker = os.path.splitext(os.path.basename(filepath))[0].upper()
        stock_df = pd.read_csv(filepath, parse_dates=['date'])

        # Ensure 'date' is datetime and normalized
        if 'date' not in stock_df.columns or 'close' not in stock_df.columns:
            continue

        stock_df['date'] = pd.to_datetime(stock_df['date'])
        stock_df.set_index('date', inplace=True)
        stock_df.index = stock_df.index.normalize()
        # print(f"{ticker} Data Date Range: {stock_df.index.min()} to {stock_df.index.max()}")
     


        stock_closes = stock_df['close'].dropna()
        common_index = stock_closes.index.intersection(qqq_closes.index)
        # print("===================")
        # print(f"Common dates between stock and QQQ: {len(common_index)}")
        if len(common_index) == 0:
            continue

        aligned_stock = stock_closes.loc[common_index].sort_index()
        aligned_ref = qqq_closes.loc[common_index].sort_index()

        rs_value = calculate_relative_strength(aligned_stock, aligned_ref, period=period)
        if rs_value is not None:
            rs_values.append((ticker, rs_value))

    # Save results
    # print("rs-----", rs_values)
    rs_df = pd.DataFrame(rs_values, columns=['ticker', 'rs_value'])
    if rs_df.empty:
        print("No data to save, skipping file creation.")
        return None

    rs_df.sort_values('rs_value', ascending=False, inplace=True)
    top_20_df = rs_df.head(20).copy()

    # Fetch sectors
    top_20_df['sector'] = [get_stock_sector(api_key, ticker) for ticker in tqdm(top_20_df['ticker'], desc="Fetching sectors")]

    try:
        top_20_df.to_excel(output_excel, index=False)
        print(f"RS results saved to {output_excel}")
        
    except Exception as e:
        print(f"Error saving file: {e}")
