
import pandas as pd

def get_previous_day_breadth_trend(file_path):
    """
    Reads an Excel file to get the most recent Primary Breadth Trend and its date.
    """
    try:
        data = pd.read_excel(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        today = pd.Timestamp('today').normalize()
        previous_day = today - pd.Timedelta(days=1)

        # Find the most recent business day with data
        while previous_day.weekday() >= 5 or previous_day not in data['Date'].values:
            previous_day -= pd.Timedelta(days=1)

        trend_row = data[data['Date'] == previous_day]
        if not trend_row.empty:
            return trend_row.iloc[0]['Primary Breadth Trend'], previous_day.strftime('%Y-%m-%d')
        else:
            return "No data available for the previous business day.", previous_day.strftime('%Y-%m-%d')
    except Exception as e:
        return f"Error reading the file: {e}", None
