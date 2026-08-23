import yfinance as yf
import pandas as pd
import numpy as np


def download_nasdaq_data():
    """
    Downloads NASDAQ (^IXIC) data using yfinance for the last 5 years.
    Calculates 52-week High/Low and McClellan Oscillator/Summation Index metrics.
    """
    nasdaq_data = yf.download('^IXIC', period='5y', group_by="ticker")

    if nasdaq_data.empty:
        print("Error: No data downloaded for NASDAQ (^IXIC).")
        return pd.DataFrame()

    nasdaq_data.columns = nasdaq_data.columns.droplevel(0)
    nasdaq_data.reset_index(inplace=True)

    nasdaq_data['52_Week_High'] = nasdaq_data['High'].rolling(window=252).max()
    nasdaq_data['52_Week_Low'] = nasdaq_data['Low'].rolling(window=252).min()

    close_values = nasdaq_data['Close'].values
    shifted_values = nasdaq_data['Close'].shift(1).values
    shifted_values[0] = close_values[0]

    advances = np.where(close_values > shifted_values, 1, 0)
    declines = np.where(close_values < shifted_values, 1, 0)
    net_advances = advances - declines
    denominator = np.where((advances + declines) == 0, 1e-6, (advances + declines))
    ratio_adjusted_net_advances = 1000 * (net_advances) / denominator
    ratio_series = pd.Series(ratio_adjusted_net_advances, index=nasdaq_data.index)

    ema_short = ratio_series.ewm(span=19, adjust=False).mean()
    ema_long = ratio_series.ewm(span=39, adjust=False).mean()

    nasdaq_data['McClellan Oscillator'] = ema_short - ema_long
    nasdaq_data['McClellan Summation Index'] = nasdaq_data['McClellan Oscillator'].cumsum()
    nasdaq_data['MSI_MA'] = nasdaq_data['McClellan Summation Index'].rolling(window=9).mean()

    nasdaq_data.dropna(inplace=True)
    return nasdaq_data


def download_qqqe_data():
    """
    Downloads QQQE (Direxion NASDAQ-100 Equal Weighted ETF) data using yfinance for
    the last 5 years. Handles MultiIndex columns and calculates EMA(10), EMA(21), EMA(50).
    """
    qqqe_data = yf.download('QQQE', period='5y', progress=False)

    if qqqe_data.empty:
        print("Error: No data downloaded for QQQE.")
        return pd.DataFrame()

    if isinstance(qqqe_data.columns, pd.MultiIndex):
        qqqe_data.columns = [col[0].lower() for col in qqqe_data.columns]
    else:
        qqqe_data.columns = [col.lower() for col in qqqe_data.columns]

    if 'close' not in qqqe_data.columns:
        print(f"Error: 'close' column not found. Available columns: {qqqe_data.columns}")
        return pd.DataFrame()

    qqqe_data['ema_10'] = qqqe_data['close'].ewm(span=10, adjust=False).mean()
    qqqe_data['ema_21'] = qqqe_data['close'].ewm(span=21, adjust=False).mean()
    qqqe_data['ema_50'] = qqqe_data['close'].ewm(span=50, adjust=False).mean()

    qqqe_data = qqqe_data[['close', 'ema_10', 'ema_21', 'ema_50']]
    qqqe_data.reset_index(inplace=True)

    return qqqe_data
