import os
import csv
import requests
from datetime import datetime
from tqdm import tqdm
from .utils import ensure_dir

def fetch_polygon_data(api_key, tickers, start_date, end_date, data_dir):
    """
    Fetches daily stock data from Polygon.io for the given tickers and saves them as CSV files.
    """
    ensure_dir(data_dir)
    
    print("\n==> [1] Fetching stock data from Polygon.io...")
    for ticker in tqdm(tickers, desc="Downloading", unit="ticker"):
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
            "apiKey": api_key
        }
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data_json = resp.json()
            if "results" in data_json:
                results = data_json["results"]
                csv_path = os.path.join(data_dir, f"{ticker}.csv")
                with open(csv_path, "w", newline="", encoding="utf-8") as cfile:
                    writer = csv.writer(cfile)
                    writer.writerow(["date", "open", "high", "low", "close", "volume"])
                    for bar in results:
                        dt = datetime.fromtimestamp(bar["t"] / 1000.0).date()
                        writer.writerow([dt, bar["o"], bar["h"], bar["l"], bar["c"], bar["v"]])
        else:
            print(f"Warning: Failed to fetch data for {ticker}. Status Code: {resp.status_code}")
    print("[1] Done fetching & saving CSV.")
