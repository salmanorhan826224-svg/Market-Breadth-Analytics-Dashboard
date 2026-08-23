# main.py

import os
import sys
import csv
from datetime import date, timedelta
import pandas as pd
from scripts.data_fetching import fetch_polygon_data
from scripts.aggregator import aggregate_and_rank_groups
from scripts.relative_strength import calculate_relative_strengths,compute_html_table_from_excel
from scripts.breadth_calculations import calculate_breadth_metrics
from scripts.annotation import get_previous_day_breadth_trend
from scripts.plotting import create_individual_charts
from scripts.scatter_plot import create_scatter_plot
from scripts.dashboard_compilation import compile_final_dashboard
from scripts.insights import create_insights_charts
from scripts.utils import ensure_dir

from config.config import (
    API_KEY,
    INPUT_UNIVERSE_FILE,
    POLYGON_DATA_DIR,
    AGGREGATED_OUTPUT_FILE,
    RS_OUTPUT_FILE,
    BREADTH_OUTPUT_FILE,
    PERCENT_ABOVE_BELOW_FILE,
    FINAL_DASHBOARD_HTML,
    SCATTER_PLOT_HTML,
    PLOTLY_DASHBOARD_HTML,
    MARKET_BREADTH_HISTORICAL_FILE,
)

from scripts.yfinance_downloads import download_nasdaq_data, download_qqqe_data

def main():
    # Read Ticker Universe
    tickers = []
    if os.path.exists(INPUT_UNIVERSE_FILE):
        with open(INPUT_UNIVERSE_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    tk = row[0].strip()
                    if tk:
                        tickers.append(tk)
    else:
        print(f"Error: Ticker file '{INPUT_UNIVERSE_FILE}' not found.")
        return

    # Define Sectors/Themes Groups
    GROUPS = {
        "Sub-Markets": {
            "Mega-Cap": "MGK",
            "Large-Cap": "SPYG",
            "Mid-Cap": "MDYG",
            "Micro-Cap": "IWC",
            "Small-Cap": "IWO"
        },
        "Sectors": {
            "Technology": "XLK",
            "Financials": "XLF",
            "Health Care": "XLV",
            "Industrial": "XLI",
            "Energy": "XLE",
            "Consumer": ["XLP", "XLY"],
            "Utilities": "XLU",
            "Oil & Gas": "XOP",
            "Materials Select": "XLB",
            "Homebuilders": "XHB",
            "Telecoms": "XTL",
            "Retail": "XRT",
            "Metals & Mining": "XME"
        },
        "Themes & Sub-Sectors": {
            "Banks": "KBWB",
            "Shipping": "SEA",
            "Natural Gas Production": "FCG",
            "Liesure & Entertainment": "PEJ",
            "Airlines": "JETS",
            "Oil & Gas Exploration & Production": "PXE",
            "Regional Banks": "KRE",
            "Wind": "FAN",
            "Aerospace & Defence": "PPA",
            "China": "PGJ",
            "Healthcare Providers": "IHF",
            "Medical Equipments": "XHE",
            "Social Media": "SOCL",
            "Natural Resources": "HAP",
            "Uranium": "URA",
            "Steel Production": "SLX",
            "Copper Producers": "COPX",
            "Metals & Mining": "XME",
            "Silver Miners": "SIL",
            "Gold": "GDX"
        }
    }

    # Define Date Range
    START_DATE = date.today() - timedelta(days=365)
    END_DATE = date.today()
    start_str = START_DATE.strftime("%Y-%m-%d")
    end_str = END_DATE.strftime("%Y-%m-%d")

    # 1) Fetch Polygon Data
    # fetch_polygon_data(API_KEY, tickers, start_str, end_str, POLYGON_DATA_DIR)

    # 2) Aggregate & Rank Groups
    dataframes =aggregate_and_rank_groups(GROUPS, API_KEY, start_str, end_str, AGGREGATED_OUTPUT_FILE)

    # 3) Relative Strength vs. QQQ
    qqq_df = download_qqqe_data() 
    qqq_df['Date'] = pd.to_datetime(qqq_df['Date'])
    qqq_df.set_index('Date', inplace=True)

    # Define date range (last 6 months)
    end_date_6m = qqq_df.index.max()
    start_date_6m = end_date_6m - timedelta(days=180)  # Approx 6 months
    qqq_df = qqq_df.loc[start_date_6m:end_date_6m]

    if qqq_df.empty:
        print("Error: QQQ data is empty. Exiting.")
    else:
        calculate_relative_strengths(
            api_key=API_KEY,
            polygon_data_dir=POLYGON_DATA_DIR,
            output_excel=RS_OUTPUT_FILE,
            qqq_df=qqq_df,
            
            period=14
        )

    # 4) Breadth Calculations
    extremes_df = calculate_breadth_metrics(POLYGON_DATA_DIR, START_DATE, END_DATE)

    # 5) Dynamic Annotation
    previous_trend, previous_date = get_previous_day_breadth_trend(MARKET_BREADTH_HISTORICAL_FILE)
    if previous_date is None:
        previous_date = "N/A"

    # 6a) Download NASDAQ and QQQE data
    nasdaq_df = download_nasdaq_data()
    if nasdaq_df.empty:
        print("Error: NASDAQ data is empty. Exiting.")
        return
    qqqe_df = download_qqqe_data()
    if qqqe_df.empty:
        print("Error: QQQE data is empty. Exiting.")
        return
    six_months_ago = END_DATE - timedelta(days=180)
    



    if isinstance(qqqe_df.columns, pd.MultiIndex):
        qqqe_df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in qqqe_df.columns.values]
        print("After flattening, qqqe_df columns:", qqqe_df.columns)
    else:
        print("qqqe_df has single-level columns:", qqqe_df.columns)

    
    if qqqe_df.index.name == 'Date' or 'Date' not in qqqe_df.columns:
        qqqe_df.reset_index(inplace=True)
        print("After resetting index, qqqe_df columns:", qqqe_df.columns)
    else:
        print("'Date' column is already present.")

    
    if 'Date' in qqqe_df.columns:
        qqqe_df['Date'] = pd.to_datetime(qqqe_df['Date'])
        print("'Date' column converted to datetime.")
    else:
        print("Error: 'Date' column is still missing after resetting index.")
        return

  
    # print("qqqe_df columns before passing to create_individual_charts:", qqqe_df.columns)
    if 'Date' not in qqqe_df.columns:
        print("Error: 'Date' column is missing in qqqe_df.")
        return
    # else:
        # print("'Date' column exists in qqqe_df.")

    # 6b) Create a market_breadth_df from extremes_df
    market_breadth_df = extremes_df[["Date", "D > 4%", "D < 4%", "5 DR", "10 DR"]].copy()

    market_breadth_df.rename(
        columns={
            "D > 4%": "Number of stocks up 4% plus",
            "D < 4%": "Number of stocks down 4% plus",
            "5 DR": "5 Day Up/Down Ratio",
            "10 DR": "10 Day Up/Down Ratio"
        },
        inplace=True
    )


    nasdaq_df = nasdaq_df[nasdaq_df['Date'] >= pd.to_datetime(six_months_ago)].copy()
    qqqe_df   = qqqe_df[qqqe_df['Date']   >= pd.to_datetime(six_months_ago)].copy()
    extremes_df = extremes_df[extremes_df['Date'] >= pd.to_datetime(six_months_ago)].copy()


    # 7) Create Individual Plotly Charts
    individual_charts = create_individual_charts(
        nasdaq_df,
        qqqe_df,
        market_breadth_df
    )

    # 8) Create Scatter Plot
    # create_scatter_plot(PERCENT_ABOVE_BELOW_FILE, SCATTER_PLOT_HTML)

    # 9) Compile Final Dashboard HTML
    compile_final_dashboard(
        individual_charts, 
        previous_trend,
        previous_date,
        FINAL_DASHBOARD_HTML,
        dataframes=dataframes
    )

    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main()
