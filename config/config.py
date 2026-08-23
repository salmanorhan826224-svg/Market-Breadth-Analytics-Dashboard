import os

# Set your Polygon.io API key as an environment variable: POLYGON_API_KEY=your_key_here
# Never hardcode API keys in source code.
API_KEY = os.environ.get("POLYGON_API_KEY", "")

# File paths
INPUT_UNIVERSE_FILE = "nasdaq_universe_polygon.csv"
POLYGON_DATA_DIR = "data/polygon_stock_data"
MARKET_BREADTH_HISTORICAL_FILE = "data/market_breadth_historical.xlsx"

# Output files
AGGREGATED_OUTPUT_FILE = "output/grouped_ranked_output.xlsx"
RS_OUTPUT_FILE = "output/rs_values_output_with_sectors.xlsx"
BREADTH_OUTPUT_FILE = "output/calculated_stock_metrics.xlsx"
PERCENT_ABOVE_BELOW_FILE = "output/percent_above_below.xlsx"

# Dashboard files
FINAL_DASHBOARD_HTML = "output/final_dashboard.html"
SCATTER_PLOT_HTML = "output/scatter_plot_200ma.html"
PLOTLY_DASHBOARD_HTML = "output/plotly_dashboard.html"
