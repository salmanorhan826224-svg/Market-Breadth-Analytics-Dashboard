import os
import pandas as pd
import plotly.graph_objects as go

def create_insights_charts():
    """
    Reads key Excel files and returns a dictionary with HTML snippets
    for each interactive chart to be included separately in the dashboard.
    """
    # Dark theme colors and common layout settings
    BACKGROUND_COLOR = '#1c1d2b'
    TEXT_COLOR = '#ffffff'
    GRID_COLOR = '#2d2e3d'
    COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#ff0000']
    layout_settings = dict(
        plot_bgcolor=BACKGROUND_COLOR,
        paper_bgcolor=BACKGROUND_COLOR,
        font=dict(color=TEXT_COLOR),
        margin=dict(t=50, l=50, r=50, b=50),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_COLOR)),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    )

    charts = {}

    # 1) Sector Rankings Chart (Legend Disabled)
    sector_rank_file = "output/grouped_ranked_output.xlsx"
    if os.path.exists(sector_rank_file):
        try:
            ranked_df = pd.read_excel(sector_rank_file, sheet_name="Ranked_Data", header=1)
            top5_ranked = ranked_df.head(5).copy()
            
            fig = go.Figure(
                data=[go.Bar(
                    x=top5_ranked['Diff_Daily'], 
                    y=top5_ranked['Sector'],
                    orientation='h',
                    marker_color=COLORS[0],
                    hovertemplate='Sector: %{y}<br>Daily Change: %{x}%<extra></extra>'
                )]
            )

            fig.update_layout(
                title="Sector/Theme Ranking (Top 5 by Daily % Change)",
                height=300,
                showlegend=False,  # Disable legend
                **layout_settings
            )

            charts['sector_rankings'] = fig.to_html(full_html=False)
        
        except Exception as e:
            charts['sector_rankings'] = f"<p style='color: white;'>Could not read {sector_rank_file}: {e}</p>"
    else:
        charts['sector_rankings'] = f"<p style='color: white;'>File not found: {sector_rank_file}</p>"

    # 2) Breadth Metrics Chart (Legend Enabled)
    breadth_metrics_file = "output/calculated_stock_metrics.xlsx"
    if os.path.exists(breadth_metrics_file):
        try:
            calc_df = pd.read_excel(breadth_metrics_file)
            included_columns = ["D > 4%", "D < 4%", "5 DR", "10 DR"]

            fig = go.Figure()
            for col in included_columns:
                if col in calc_df.columns:
                    fig.add_trace(go.Scatter(
                        x=calc_df['Date'],
                        y=calc_df[col],
                        name=col,
                        line=dict(color=COLORS[calc_df.columns.get_loc(col) % len(COLORS)])
                    ))

            fig.update_layout(
                title="Recent Breadth Metrics (Last 5 Business Days)",
                height=300,
                **layout_settings
            )
            charts['breadth_metrics'] = fig.to_html(full_html=False)
        except Exception as e:
            charts['breadth_metrics'] = f"<p style='color: white;'>Could not read {breadth_metrics_file}: {e}</p>"
    else:
        charts['breadth_metrics'] = f"<p style='color: white;'>File not found: {breadth_metrics_file}</p>"

    # 3) Stocks Above 200MA Chart (Legend Disabled)
    stocks_ma_file = "output/percent_above_below.xlsx"
    if os.path.exists(stocks_ma_file):
        try:
            above_df = pd.read_excel(stocks_ma_file)
            top5_above = above_df.sort_values("percent_above_below", ascending=False).head(10)
            fig = go.Figure(data=[go.Bar(
                x=top5_above['stock'],
                y=top5_above['percent_above_below'],
                marker_color=COLORS[2],
                hovertemplate='Stock: %{x}<br>% Above/Below 200 MA: %{y:.2f}%<extra></extra>'
            )])

            fig.update_layout(
                title="Top 10 Stocks Above 200-Day MA",
                height=300,
                showlegend=False,  # Disable legend
                **layout_settings
            )

            charts['stocks_above_200ma'] = fig.to_html(full_html=False)
        except Exception as e:
            charts['stocks_above_200ma'] = f"<p style='color: white;'>Could not read {stocks_ma_file}: {e}</p>"
    else:
        charts['stocks_above_200ma'] = f"<p style='color: white;'>File not found: {stocks_ma_file}</p>"

  
    # 4) Relative Strength vs. QQQ Chart 
    rs_file = "output/rs_values_output_with_sectors.xlsx"
    if os.path.exists(rs_file):
        try:
            rs_df = pd.read_excel(rs_file)
            sorted_rs = rs_df.sort_values('rs_value', ascending=False).head(10)
            fig = go.Figure(data=[
                go.Bar(
                    x=sorted_rs['ticker'],
                    y=sorted_rs['rs_value'],
                    marker_color=COLORS[3],
                    hovertemplate='Ticker: %{x}<br>RS Value: %{y:.2f}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Top 10 Stocks by Relative Strength vs. QQQ",
                height=300,
                **layout_settings
            )
            charts['relative_strength'] = fig.to_html(full_html=False)
        except Exception as e:
            charts['relative_strength'] = f"<p style='color: white;'>Could not read {rs_file}: {e}</p>"
    else:
        charts['relative_strength'] = f"<p style='color: white;'>File not found: {rs_file}</p>"

    return charts
