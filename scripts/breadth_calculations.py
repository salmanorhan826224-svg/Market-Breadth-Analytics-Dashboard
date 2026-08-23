import os
import pandas as pd
from tqdm import tqdm
import numpy as np
from .utils import ensure_dir

def calculate_breadth_metrics(polygon_data_dir, start_date, end_date):
    """
    Calculates breadth metrics including % above 200-day MA, additional SMA stats, and daily extremes.
    Saves results to Excel.
    """
    print("\n==> [4] Calculating % Above/Below 200-Day MA...")
    plot_data = []
    all_files = [f for f in os.listdir(polygon_data_dir) if f.endswith(".csv")]
    for fn in tqdm(all_files, desc="200MA Calculation", unit="file"):
        fpath = os.path.join(polygon_data_dir, fn)
        df_ = pd.read_csv(fpath)
        if "date" in df_.columns and "close" in df_.columns:
            df_["date"] = pd.to_datetime(df_["date"])
            df_.sort_values("date", inplace=True)
            df_["200_MA"] = df_["close"].rolling(window=200).mean()
            stock_name = os.path.splitext(fn)[0].upper()
            if len(df_) >= 200:
                last_price = df_["close"].iloc[-1]
                last_ma = df_["200_MA"].iloc[-1]
                if not np.isnan(last_ma):
                    pct_diff = ((last_price - last_ma) / last_ma) * 100
                    plot_data.append({
                        "stock": stock_name,
                        "last_price": last_price,
                        "percent_above_below": pct_diff
                    })
    df_200 = pd.DataFrame(plot_data)
    df_200.sort_values("percent_above_below", ascending=False, inplace=True)
    # Label top 20
    top20_200 = df_200.head(20).index
    df_200["label"] = ""
    df_200.loc[top20_200, "label"] = df_200["stock"]
    
    # Save df_200 to a separate Excel file for the scatter plot
    percent_above_below_file = "output/percent_above_below.xlsx"
    df_200.to_excel(percent_above_below_file, index=False)
    print(f"[4] % Above/Below 200-Day MA saved to: {percent_above_below_file}")
    
    # Additional Breadth Stats: % above 5/50/200 SMA
    print("\n==> [5] Calculating Additional Breadth Stats (% above 5/50/200 SMA)...")
    def breadth_sma(csv_file):
        dfx = pd.read_csv(csv_file, parse_dates=["date"])
        dfx.sort_values("date", inplace=True)
        dfx["5_SMA"] = dfx["close"].rolling(5).mean()
        dfx["50_SMA"] = dfx["close"].rolling(50).mean()
        dfx["200_SMA"] = dfx["close"].rolling(200).mean()
        last = dfx.iloc[-1]
        # Handle NaNs
        above5 = (last["close"] > last["5_SMA"]) if not np.isnan(last["5_SMA"]) else False
        above50 = (last["close"] > last["50_SMA"]) if not np.isnan(last["50_SMA"]) else False
        above200 = (last["close"] > last["200_SMA"]) if not np.isnan(last["200_SMA"]) else False
        return above5, above50, above200
    
    files_ = [os.path.join(polygon_data_dir, f) for f in os.listdir(polygon_data_dir) if f.endswith(".csv")]
    count_5 = 0
    count_50 = 0
    count_200 = 0
    valid_tickers = 0
    
    for f in tqdm(files_, desc="Breadth SMA Calculation", unit="file"):
        try:
            a5, a50, a200 = breadth_sma(f)
            valid_tickers += 1
            if a5: count_5 += 1
            if a50: count_50 += 1
            if a200: count_200 += 1
        except:
            pass
    
    pct_5   = round((count_5/valid_tickers)*100, 2) if valid_tickers else 0
    pct_50  = round((count_50/valid_tickers)*100, 2) if valid_tickers else 0
    pct_200 = round((count_200/valid_tickers)*100, 2) if valid_tickers else 0
    
    print(f"[5] {valid_tickers} valid tickers. %Above 5 SMA: {pct_5}%, 50 SMA: {pct_50}%, 200 SMA: {pct_200}%")
    
    # Daily extremes (4% up/down, 25% in 90 Days)
    print("\n==> [6] Calculating Daily Extremes (4% Up/Down, 25% in 90 Days)...")
    stock_list = [os.path.splitext(x)[0] for x in os.listdir(polygon_data_dir) if x.endswith(".csv")]
    stock_data_map = {}
    
    # Read all data once
    for s in tqdm(stock_list, desc="Loading Stock Data", unit="stock"):
        f_ = os.path.join(polygon_data_dir, s + ".csv")
        df_ = pd.read_csv(f_, parse_dates=["date"])
        df_.set_index("date", inplace=True)
        df_.sort_index(inplace=True)
        stock_data_map[s] = df_
    
    all_dates = pd.date_range(start=start_date, end=end_date, freq="B")
    extremes_records = []
    for d_ in tqdm(all_dates, desc="Computing Extremes", unit="date"):
        day_str = d_.strftime("%Y-%m-%d")
        count_up4 = 0
        count_dn4 = 0
        count_up25 = 0
        count_dn25 = 0

        for s_, df_ in stock_data_map.items():
            if day_str in df_.index:
                loc_ = df_.index.get_loc(day_str)
                if isinstance(loc_, slice):
                    # In case of multiple entries
                    loc_ = loc_.start
                if loc_ == 0:
                    continue
                close_today = df_.iloc[loc_]["close"]
                close_yday = df_.iloc[loc_-1]["close"]
                daily_pct = ((close_today - close_yday)/close_yday)*100
                if daily_pct >= 4:
                    count_up4 += 1
                elif daily_pct <= -4:
                    count_dn4 += 1

                # 90-day change
                if loc_ >= 90:
                    close_90ago = df_.iloc[loc_ - 90]["close"]
                    if close_90ago != 0:
                        pct_90 = ((close_today - close_90ago)/close_90ago)*100
                        if pct_90 >= 25:
                            count_up25 += 1
                        elif pct_90 <= -25:
                            count_dn25 += 1

        extremes_records.append({
            "Date": d_,
            "D > 4%": count_up4,
            "D < 4%": count_dn4,
            "Q > 25%": count_up25,
            "Q < 25%": count_dn25
        })

    extremes_df = pd.DataFrame(extremes_records)
    extremes_df.sort_values("Date", inplace=True)
    extremes_df.reset_index(drop=True, inplace=True)
    extremes_df["5 DR"] = extremes_df["D > 4%"].rolling(window=5).sum() / extremes_df["D < 4%"].rolling(window=5).sum()
    extremes_df["10 DR"] = extremes_df["D > 4%"].rolling(window=10).sum() / extremes_df["D < 4%"].rolling(window=10).sum()
    extremes_df.fillna(0, inplace=True)

    extremes_out = "output/calculated_stock_metrics.xlsx"
    extremes_df.to_excel(extremes_out, index=False)
    print(f"[6] Daily extremes saved to: {extremes_out}")
    
    return extremes_df
