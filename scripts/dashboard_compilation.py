import os
import sys
import subprocess
from scripts.insights import create_insights_charts
import plotly.graph_objects as go
import pandas as pd
from bs4 import BeautifulSoup


import plotly.graph_objects as go
from bs4 import BeautifulSoup


def compile_final_dashboard(individual_charts, previous_trend, previous_date, output_html, dataframes=None):
    """
    Compiles all individual Plotly plots, scatter plot, and insights into a single HTML file
    with an improved dark theme and modern layout.

    Args:
        individual_charts (dict): Dictionary of Plotly figures.
        previous_trend (str): The previous trend value (e.g., "Bullish" or "Bearish").
        previous_date (str): The date of the previous trend.
        output_html (str): Path to save the final HTML dashboard.
        tables_html (dict): Optional dictionary of HTML tables to include at the end.
    """
    print("\n==> [8] Compiling Final Dashboard HTML...")

#     # Generate Insights Charts
#     insights_charts = create_insights_charts()

#     # Enhanced Styling with Modern Dark Theme
#     html_style = """
#     <style>
#         :root {
#             --primary-bg: #13141f;
#             --card-bg: #1c1d2b;
#             --accent-purple: #8b5cf6;
#             --text-primary: #ffffff;
#             --text-secondary: #9ca3af;
#             --card-border: #2d2e3d;
#         }

#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }

#         body {
#             background-color: var(--primary-bg);
#             color: var(--text-primary);
#             font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#             line-height: 1.6;
#             height: 100vh;
#             display: flex;
#             flex-direction: column;
#             overflow: hidden;
#         }

#         .dashboard-header {
#             display: flex;
#             align-items: center;
#             justify-content: flex-end;
#             padding: 1rem;
#             position: absolute; 
#             top: 0; 
#             left: 0;
#             width: 100%; 
#             z-index: 100; 
#         }

#         .header-title {
#             font-size: 1.25rem;
#             font-weight: 600;
#             color: var(--text-primary);
#         }

#         .trend-card {
#             background-color: rgba(0, 0, 0, 0.5); /* Add a semi-transparent black background */
#             border-bottom: none; /* Remove the border */
#             padding: 0.5rem 1rem;
#             border-radius: 0.5rem;
#             border: 1px solid var(--card-border);
#         }

#         .trend-title {
#             color: var(--accent-purple);
#             font-size: 0.875rem;
#             margin-bottom: 0.25rem;
#         }

#         .trend-value {
#             font-size: 1.125rem;
#             font-weight: 600;
#             color: var(--text-primary);
#             display: flex;
#             align-items: center;
#             gap: 0.5rem;
#         }

#         .trend-date {
#             color: var(--text-secondary);
#             font-size: 0.75rem;
#             font-style: italic;
#         }

#         .dashboard-content {
#             flex: 1;
#             padding: 1rem;
#             overflow-y: auto;
#         }

#         .grid-container {
#             display: grid;
#             grid-template-columns: repeat(3, 1fr);
#             gap: 1rem;
#             height: 100%;
#         }

#         .chart-card {
#             background-color: var(--card-bg);
#             border-radius: 0.5rem;
#             border: 1px solid var(--card-border);
#             padding: 1rem;
#             display: flex;
#             flex-direction: column;
#         }

#         .chart-title {
#             font-size: 0.875rem;
#             font-weight: 600;
#             color: var(--text-primary);
#             margin-bottom: 0.5rem;
#         }

#         .chart-content {
#             flex: 1;
#             min-height: 0;
#         }

#         .span-2 {
#             grid-column: span 2;
#         }

#         .chart-card iframe {
#             width: 100%;
#             height: 100%;
#             border: none;
#         }

#         .tables-section {
#             margin-top: 2rem;
#             padding: 1rem;
#             background-color: var(--card-bg);
#             border-radius: 0.5rem;
#             border: 1px solid var(--card-border);
#         }

#         .tables-section h2 {
#             font-size: 1.25rem;
#             font-weight: 600;
#             color: var(--text-primary);
#             margin-bottom: 1rem;
#         }

#         .data-table {
#             width: 100%;
#             border-collapse: collapse;
#             margin: 1rem 0;
#             color: var(--text-primary);
#         }

#         .data-table th, .data-table td {
#             padding: 0.75rem;
#             text-align: left;
#             border-bottom: 1px solid var(--card-border);
#         }

#         .data-table th {
#             background-color: var(--card-bg);
#             font-weight: 600;
#         }

#         .data-table tr:hover {
#             background-color: var(--card-bg);
#         }

#         @media (max-width: 1024px) {
#             .grid-container {
#                 grid-template-columns: 1fr;
#             }

#             .span-2 {
#                 grid-column: span 1;
#             }
#         }
#     </style>
#     """

#     # Arrow icons for trends
#     arrow_icons = """
#     <svg style="display: none;">
#         <symbol id="arrow-up" viewBox="0 0 24 24">
#             <path fill="currentColor" d="M7 14l5-5 5 5z"/>
#         </symbol>
#         <symbol id="arrow-down" viewBox="0 0 24 24">
#             <path fill="currentColor" d="M7 10l5 5 5-5z"/>
#         </symbol>
#     </svg>
#     """

#     # Assemble chart sections
#     chart_sections = ""
    
#     # Add individual charts
#     for name, fig in individual_charts.items():
#         plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
#         chart_sections += f"""
#         <div class="chart-card">
#             <h2 class="chart-title">{name}</h2>
#             <div class="chart-content">{plot_html}</div>
#         </div>
#         """

#     # Add insights charts
#     for chart_key, chart_html in insights_charts.items():
#         chart_sections += f"""
#         <div class="chart-card">
#             <div class="chart-content">{chart_html}</div>
#         </div>
#         """

#     # Trend indicator class
#     trend_indicator = "text-green-500" if "bullish" in previous_trend.lower() else "text-red-500"

#     # Assemble tables section
#     tables_section = ""
#     # print(dataframes)
#     if dataframes:
#         for group, df in dataframes.items():
#             table_html = f"""
#             <div class='tables-section'>
#                 <h3>{group}</h3>
#                 <table border='1' style='border-collapse: collapse; width: 100%; color: white; background-color: black;'>
#                     <tr style='background-color: coral;'>
#                         {''.join(f'<th>{col}</th>' for col in df.columns)}
#                     </tr>
#                     {''.join(f'<tr>{''.join(f'<td>{value}</td>' for value in row)}</tr>' for row in df.values)}
#                 </table>
#             </div>
#             """
#             tables_section += table_html

#     # Assemble final HTML
#     final_html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Market Analytics Dashboard</title>
#     {html_style}
#     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
# </head>
# <body>
#     {arrow_icons}
#     <header class="dashboard-header">
#         <div class="trend-card">
#             <div class="trend-value">
#                 {previous_trend}
#                 <svg class="{trend_indicator}" width="20" height="20">
#                     <use href="#{'arrow-up' if 'bullish' in previous_trend.lower() else 'arrow-down'}"/>
#                 </svg>
#             </div>
#             <p class="trend-date">Date: {previous_date}</p>
#         </div>
#     </header>

#     <main class="dashboard-content">
#         <div class="grid-container">
#             {chart_sections}
      
#         <div>
#         {tables_section}
#           </div>
#     </main>
# </body>
# </html>
# """

#     try:
#         with open(output_html, "w", encoding="utf-8") as f:
#             f.write(final_html_content)
#         print(f"[9] Final dashboard compiled and saved to: {output_html}")
#     except Exception as e:
#         print(f"Error writing to file: {e}")
#     """
#     Compiles all individual Plotly plots, scatter plot, and insights into a single HTML file
#     with an improved dark theme and modern layout.

#     Args:
#         individual_charts (dict): Dictionary of Plotly figures.
#         previous_trend (str): The previous trend value (e.g., "Bullish" or "Bearish").
#         previous_date (str): The date of the previous trend.
#         output_html (str): Path to save the final HTML dashboard.
#         tables_html (str): Optional HTML content for tables to include at the end.
#     """
#     print("\n==> [9] Compiling Final Dashboard HTML...")

    # Generate Insights Charts
    insights_charts = create_insights_charts()

    # Enhanced Styling with Modern Dark Theme
    html_style = """
    <style>
        :root {
    --primary-bg: #000000; /* Black background */
    --card-bg: #1a1a1a; /* Dark gray for cards */
    --accent-purple: #8b5cf6; /* Accent color */
    --text-primary: #ffffff; /* White text */
    --text-secondary: #9ca3af; /* Light gray text */
    --card-border: #2d2e3d; /* Border color */
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--primary-bg);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.dashboard-header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 1rem;
    position: absolute; 
    top: 0; 
    left: 0;
    width: 100%; 
    z-index: 100; 
}

.header-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.trend-card {
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
    border-bottom: none; 
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    border: 1px solid var(--card-border);
}

.trend-title {
    color: var(--accent-purple);
    font-size: 0.875rem;
    margin-bottom: 0.25rem;
}

.trend-value {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.trend-date {
    color: var(--text-secondary);
    font-size: 0.75rem;
    font-style: italic;
}

.dashboard-content {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 2rem; /* Spacing between sections */
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    height: auto; /* Adaptive height */
}

.chart-card {
    background-color: var(--card-bg);
    border-radius: 0.5rem;
    border: 1px solid var(--card-border);
    padding: 1rem;
    display: flex;
    flex-direction: column;
}

.chart-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.chart-content {
    flex: 1;
    min-height: 0;
    height: auto; /* Adaptive height for charts */
}

.span-2 {
    grid-column: span 2;
}

.chart-card iframe {
    width: 100%;
    height: 100%; /* Ensure charts fill the container */
    border: none;
}

.tables-section {
    margin-top: 2rem; /* Spacing from charts */
    padding: 1rem;
    background-color: var(--card-bg);
    border-radius: 0.5rem;
    border: 1px solid var(--card-border);
}

.tables-section h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    color: var(--text-primary);
}

.data-table th, .data-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--card-border);
}

.data-table th {
    background-color: var(--card-bg);
    font-weight: 600;
}

.data-table tr:hover {
    background-color: var(--card-bg);
}

@media (max-width: 1024px) {
    .grid-container {
        grid-template-columns: 1fr;
    }

    .span-2 {
        grid-column: span 1;
    }
}
    </style>
    """

    # Arrow icons for trends
    arrow_icons = """
    <svg style="display: none;">
        <symbol id="arrow-up" viewBox="0 0 24 24">
            <path fill="currentColor" d="M7 14l5-5 5 5z"/>
        </symbol>
        <symbol id="arrow-down" viewBox="0 0 24 24">
            <path fill="currentColor" d="M7 10l5 5 5-5z"/>
        </symbol>
    </svg>
    """

    # Assemble chart sections
    chart_sections = ""
    
    # Add individual charts
    for name, fig in individual_charts.items():
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        chart_sections += f"""
        <div class="chart-card">
            <h2 class="chart-title">{name}</h2>
            <div class="chart-content">{plot_html}</div>
        </div>
        """

    # Add insights charts
    for chart_key, chart_html in insights_charts.items():
        chart_sections += f"""
        <div class="chart-card">
            <div class="chart-content">{chart_html}</div>
        </div>
        """

    # Trend indicator class
    trend_indicator = "text-green-500" if "bullish" in previous_trend.lower() else "text-red-500"



    tables_section = ""
    if dataframes:
        for group, df in dataframes.items():
            # Convert DataFrame to Plotly table
            plotly_table = go.Table(
                header=dict(
                    values=df.columns.tolist(),
                    align='left',
                    fill_color='#1a1a1a',  # Dark gray background for header
                    font=dict(color='white', size=12)  # White text for header
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],
                    align='left',
                    fill_color='#2d2d2d',  # Slightly lighter gray background for cells
                    font=dict(color='white', size=11)  # White text for cells
                )
            )
            plotly_fig = go.Figure(data=[plotly_table])
            plotly_fig.update_layout(
                # title=f"{group}",
                margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor='#000000',  # Black background for the entire table
                plot_bgcolor='#000000',  # Black background for the plot area
                font=dict(color='white')  # White text for the title
            )
            plotly_html = plotly_fig.to_html(full_html=False, include_plotlyjs='cdn')

            tables_section += f"""
            <div class="tables-section">
                <h2>{group}</h2>
                <div class="chart-content">{plotly_html}</div>
            </div>
            """

    # Assemble final HTML
    final_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Analytics Dashboard</title>
    {html_style}
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    {arrow_icons}
    <header class="dashboard-header">
        <div class="trend-card">
            <div class="trend-value">
                {previous_trend}
                <svg class="{trend_indicator}" width="20" height="20">
                    <use href="#{'arrow-up' if 'bullish' in previous_trend.lower() else 'arrow-down'}"/>
                </svg>
            </div>
            <p class="trend-date">Date: {previous_date}</p>
        </div>
    </header>

    <main class="dashboard-content">
        <div class="grid-container">
            {chart_sections}
        </div>
       <h2 style="padding:16px">Grouped Ranking</h2>


        {tables_section}  
            </main>
</body>
</html>
"""

    try:
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(final_html_content)
        print(f"[9] Final dashboard compiled and saved to: {output_html}")
    except Exception as e:
        print(f"Error writing to file: {e}")