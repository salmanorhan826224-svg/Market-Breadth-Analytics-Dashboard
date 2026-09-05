# Market Breadth and Relative Strength Analytics Dashboard

<div align="center">

[<img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License">](https://opensource.org/licenses/Apache-2.0)
<img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB.svg?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Dashboard-Streamlit%20%7C%20Plotly-FF4B4B.svg?logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/Market%20Telemetry-Breadth%20%26%20Relative%20Strength-0052FF.svg" alt="Telemetry">
<img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg" alt="Status">

**Enterprise-grade, high-performance implementation built and maintained by Muhammad Salman.**

[Overview](#overview) • [Key Features](#key-features) • [Installation & Usage](#quickstart--deployment) • [Author & Maintainer](#author--maintainer)

</div>

---

A systematic market analytics platform that collects daily OHLCV data for the full NASDAQ universe (3,941 stocks), computes market breadth metrics, relative strength rankings, and McClellan oscillator signals, and compiles everything into an interactive Plotly HTML dashboard. The pipeline runs end-to-end from a single command.

---

## Overview

This tool is designed for quantitative equity researchers and market analysts who need a broad, data-driven view of overall market health — beyond what any single index price can reveal. Instead of tracking where the market is, this system tracks how many stocks are participating in a trend, which sectors are leading, and which individual names are showing the highest momentum relative to a benchmark.

The full data pipeline covers four main areas:

- **Data collection** — Downloads daily OHLCV data for all tracked tickers from Polygon.io
- **Breadth analysis** — Computes what percentage of stocks are above key moving averages and flags breadth extremes
- **Relative strength** — Ranks every stock by its RS ratio against the QQQE equal-weight benchmark
- **Dashboard compilation** — Assembles all charts and ranking tables into a dark-themed interactive HTML dashboard

---

## What the Dashboard Shows

The compiled dashboard contains six main analytical sections:

### 1. Market Breadth — Stocks Above Key Moving Averages

For each trading day, the pipeline calculates the percentage of NASDAQ stocks trading above their 5-day, 50-day, and 200-day simple moving averages. These are plotted as time-series lines alongside the QQQE price chart.

A rising percentage of stocks above the 200-day SMA signals broad market participation in an uptrend. A falling percentage signals distribution even if the index itself is holding up.

### 2. McClellan Oscillator and Summation Index

The McClellan Oscillator is calculated from advancing versus declining stocks on the NASDAQ each day. It is derived by applying 19-day and 39-day exponential moving averages to the ratio-adjusted net advances and subtracting one from the other.

The Summation Index is the running cumulative sum of the oscillator. A rising Summation Index with a reading above zero confirms a healthy, expanding market. A declining Summation Index warns of underlying deterioration.

Both are plotted as separate interactive Plotly charts with a 9-day moving average overlay on the Summation Index.

### 3. 52-Week High / Low Chart

This chart counts the number of NASDAQ stocks hitting new 52-week highs versus new 52-week lows each day, displayed as a histogram. Persistently more new highs than new lows is the baseline condition of a healthy bull market.

### 4. Relative Strength Rankings (vs. QQQE)

Each stock in the NASDAQ universe is scored by its relative strength against the QQQE equal-weight benchmark using a ratio-based RS calculation over a 14-day lookback. The top 20 highest-RS stocks are written to an Excel output file and plotted in the dashboard.

Ranking against an equal-weight index (QQQE) rather than the cap-weighted QQQ removes the dominance of mega-cap names and identifies stocks that are genuinely outperforming on a stock-level, not because of index concentration.

### 5. Sector and Theme ETF Rankings

A curated list of sector and theme ETFs is evaluated for short-term and medium-term momentum: 1-day return, 5-day return, 1-month return, 3-month return, and 52-week range position. Results are written to Excel with conditional color formatting and displayed as a top-5 sector ranking chart in the dashboard.

This section allows rapid identification of which sectors are in relative strength and which are underperforming the broader market.

### 6. Breadth Extreme Detectors

Two extreme conditions are tracked:

- **4% single-day moves**: Counts how many stocks gained or lost more than 4% in a single trading session. A spike in 4%-down stocks signals panic; a spike in 4%-up stocks signals a potential breadth thrust.
- **25% moves over 90 days**: Identifies stocks that have rallied or sold off more than 25% over the past 90 calendar days, with 5-day and 10-day tallies to detect momentum clusters.

---

## Data Pipeline Architecture

The pipeline is orchestrated by `main.py` and runs twelve modules in sequence:

```
main.py
 |
 |-- 1. data_fetching.py          Fetch daily OHLCV from Polygon.io REST API for all tickers
 |-- 2. yfinance_downloads.py     Download NASDAQ index (^IXIC) and QQQE via yfinance
 |-- 3. aggregator.py             Fetch sector/theme ETF data, rank by momentum, export to Excel
 |-- 4. relative_strength.py      Compute RS ratio vs QQQE for each stock, export top 20 to Excel
 |-- 5. breadth_calculations.py   Compute % above SMAs, 4%/25% extremes, export to Excel
 |-- 6. annotation.py             Read historical breadth Excel, extract latest trend annotation
 |-- 7. plotting.py               Build individual Plotly figures (McClellan, 52wk H/L, QQQE+EMA)
 |-- 8. scatter_plot.py           Build 200MA scatter plot (all stocks by % distance from 200 SMA)
 |-- 9. insights.py               Build insight chart HTML snippets from Excel outputs
 |-- 10. dashboard_compilation.py  Assemble all charts + ranking tables into final dark HTML dashboard
 |-- 11. utils.py                  Shared utility functions (directory creation, safe CSV reading)
```

Each module writes its output to either the `data/`, `output/`, or a generated HTML file. Running `main.py` once regenerates every output from scratch.

---

## Project Structure

```
market-breadth-dashboard/
├── main.py                              # Pipeline orchestrator — run this
├── requirements.txt                     # Python dependencies
├── .env.example                         # API key template — copy to .env
├── nasdaq_universe_polygon.csv          # Full NASDAQ ticker universe (3,941 tickers)
├── nasdaq_short.csv                     # Short test universe for development
├── config/
│   └── config.py                        # File paths and API key (reads from env)
├── scripts/
│   ├── data_fetching.py                 # Polygon.io OHLCV downloader
│   ├── yfinance_downloads.py            # NASDAQ index + QQQE downloader
│   ├── aggregator.py                    # Sector/ETF momentum rankings
│   ├── relative_strength.py             # RS vs QQQE calculator
│   ├── breadth_calculations.py          # % above SMA + extreme detectors
│   ├── annotation.py                    # Historical breadth trend reader
│   ├── plotting.py                      # Individual Plotly chart builders
│   ├── scatter_plot.py                  # 200MA scatter chart
│   ├── insights.py                      # Insight chart HTML builder
│   ├── dashboard_compilation.py         # Full dashboard assembler
│   └── utils.py                         # Shared utilities
├── data/
│   ├── market_breadth_historical.xlsx   # Historical breadth data (hand-maintained)
│   ├── market_breadth_historical_new.xlsx
│   └── polygon_stock_data/              # Per-ticker OHLCV CSVs (3,941 files)
│       ├── AAPL.csv
│       ├── MSFT.csv
│       └── ...
└── output/
    ├── calculated_stock_metrics.xlsx    # Breadth metrics per stock
    ├── grouped_ranked_output.xlsx       # Sector/ETF rankings with formatting
    ├── percent_above_below.xlsx         # % above each SMA over time
    └── rs_values_output_with_sectors.xlsx  # RS rankings with sector labels
```

---

## OHLCV Data Format

Each file in `data/polygon_stock_data/` follows this structure:

```
date,open,high,low,close,volume
2020-01-02,296.24,300.60,296.00,300.35,33870100
2020-01-03,297.15,300.58,296.50,297.43,36580600
...
```

Data is sourced from the Polygon.io REST API and covers available history through the last fetch date. The included dataset contains 3,941 NASDAQ-listed tickers.

---

## Getting Started

**Step 1: Clone the repository**
```bash
git clone https://github.com/salmanorhan826224-svg/market-breadth-dashboard.git
cd market-breadth-dashboard
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Set your Polygon.io API key**

Copy `.env.example` to `.env` and fill in your key:
```bash
cp .env.example .env
```

Then edit `.env`:
```
POLYGON_API_KEY=your_polygon_api_key_here
```

A free Polygon.io key is available at [polygon.io](https://polygon.io). The free tier provides end-of-day data which is sufficient for all calculations in this pipeline.

**Step 4: Load your API key into the environment**
```bash
# Linux/macOS
export POLYGON_API_KEY=your_key_here

# Windows PowerShell
$env:POLYGON_API_KEY = "your_key_here"
```

**Step 5: Run the full pipeline**
```bash
python main.py
```

This runs all twelve modules in sequence. On first run, data fetching for the full 3,941-ticker universe will take approximately 30–60 minutes depending on your internet connection and API rate limits. Subsequent runs that skip fetching (by commenting out the fetch step in `main.py`) complete in under two minutes.

**Step 6: Open the dashboard**

```bash
# Open the compiled dashboard in your browser
output/final_dashboard.html
```

The dashboard is a fully self-contained HTML file with embedded Plotly JavaScript — no server required, no internet connection required to view it after generation.

---

## Output Files

| File | Description |
|---|---|
| `output/final_dashboard.html` | Full compiled interactive dashboard with all charts and tables |
| `output/plotly_dashboard.html` | Standalone Plotly breadth chart |
| `output/scatter_plot_200ma.html` | Interactive scatter of all stocks by % distance from 200 SMA |
| `output/calculated_stock_metrics.xlsx` | Per-stock breadth metrics (above/below SMAs, extremes) |
| `output/grouped_ranked_output.xlsx` | Sector/ETF momentum rankings with conditional formatting |
| `output/percent_above_below.xlsx` | Historical daily % above each SMA across the universe |
| `output/rs_values_output_with_sectors.xlsx` | RS rankings with sector and industry labels |

---

## Skipping Data Fetching

If you already have data in `data/polygon_stock_data/` (as included in this repo), you can skip the fetch step and go straight to calculations by commenting out the `data_fetching` call in `main.py`. This is the recommended approach for iterating on the breadth calculations or dashboard styling without re-downloading all data.

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Market Data | Polygon.io REST API, yfinance |
| Data Processing | pandas, numpy |
| Progress Tracking | tqdm |
| Visualization | Plotly (interactive HTML charts) |
| Excel Output | openpyxl (with conditional formatting) |
| Dashboard Assembly | BeautifulSoup4, Plotly |
| API Communication | requests |

---

---

---

## Author & Maintainer

**Muhammad Salman**  
*Business Developer & Data Analyst*  
**

* **Email**: [salmanorhan826224@gmail.com](mailto:salmanorhan826224@gmail.com)
* **LinkedIn**: [linkedin.com/in/muhammad-salman-9a6052301](https://www.linkedin.com/in/muhammad-salman-9a6052301)
* **GitHub**: [github.com/salmanorhan826224-svg](https://github.com/salmanorhan826224-svg)

