import plotly.graph_objects as go
import pandas as pd

def create_individual_charts(nasdaq_df, qqqe_df, market_breadth_df):
    """
    Creates individual Plotly figures for each dataset, returning
    them as a dictionary of { chart_name: figure }.
    """
    charts = {}
    print("[7] Ploting Graphs....")


    market_breadth_df["Date"] = pd.to_datetime(market_breadth_df["Date"])
    nasdaq_df["Date"] = pd.to_datetime(nasdaq_df["Date"])
    qqqe_df["Date"] = pd.to_datetime(qqqe_df["Date"])

    # 1. 52-Week High/Low
    fig_high_low = go.Figure()
    fig_high_low.add_trace(go.Scatter(
        x=nasdaq_df["Date"], y=nasdaq_df["52_Week_High"],
        mode="lines", name="52-Week High", line=dict(color="cyan")
    ))
    fig_high_low.add_trace(go.Scatter(
        x=nasdaq_df["Date"], y=nasdaq_df["52_Week_Low"],
        mode="lines", name="52-Week Low", line=dict(color="orange")
    ))
    fig_high_low.update_layout(
        title="52-Week High/Low", template='plotly_dark',
        height=300, margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    charts['high_low'] = fig_high_low

    # 2a. McClellan Oscillator (Bar Chart Only)
    fig_mcclellan_osc = go.Figure()
    fig_mcclellan_osc.add_trace(go.Bar(
        x=nasdaq_df["Date"], y=nasdaq_df["McClellan Oscillator"],
        name="McClellan Oscillator", marker_color="lightgreen", opacity=0.6
    ))
    fig_mcclellan_osc.update_layout(
        title="McClellan Oscillator (Histogram)", template='plotly_dark',
        height=300, margin=dict(l=40, r=40, t=40, b=40),
        yaxis_title="McClellan Oscillator",
        showlegend=False
    )
    charts['mcclellan_osc'] = fig_mcclellan_osc

    # 2b. McClellan Summation Index
    fig_mcclellan_sum = go.Figure()
    fig_mcclellan_sum.add_trace(go.Scatter(
        x=nasdaq_df["Date"], y=nasdaq_df["McClellan Summation Index"],
        mode="lines", name="McClellan Summation Index",
        line=dict(color="yellow", width=2)
    ))
    fig_mcclellan_sum.add_trace(go.Scatter(
        x=nasdaq_df["Date"], y=nasdaq_df["MSI_MA"],
        mode="lines", name="MSI_MA (9-day)",
        line=dict(color="magenta", dash="dash")
    ))
    fig_mcclellan_sum.update_layout(
        title="McClellan Summation Index", template='plotly_dark',
        height=300, margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    charts['mcclellan_sum'] = fig_mcclellan_sum

    # 3. QQQE Price & EMAs
    fig_qqqe = go.Figure()
    column_mapping = {
    "Close_QQQE": "close",  # Adjusting for lowercase
    "EMA_10": "ema_10",
    "EMA_21": "ema_21",
    "EMA_50": "ema_50"
}

    for col, color, style in zip(column_mapping.keys(),
                                ["white", "blue", "cyan", "gold"],
                                ["solid", "solid", "solid", "solid"]):
        if column_mapping[col] in qqqe_df.columns:
            fig_qqqe.add_trace(go.Scatter(
                x=qqqe_df["Date"], y=qqqe_df[column_mapping[col]],
                mode='lines', name=col.replace("_", " "),
                line=dict(color=color, width=1.5, dash=style)
            ))

    fig_qqqe.update_layout(
        title="QQQE Price & EMAs", template='plotly_dark',
        height=300, margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    charts['qqqe'] = fig_qqqe

    # 4a. Market Breadth: Stocks Up/Down 4% (Bar Chart)
    fig_breadth_up_down = go.Figure()
    fig_breadth_up_down.add_trace(go.Bar(
        x=market_breadth_df["Date"],
        y=market_breadth_df["Number of stocks up 4% plus"],
        name="Stocks Up 4%", marker_color="lightgreen", opacity=0.6
    ))
    fig_breadth_up_down.add_trace(go.Bar(
        x=market_breadth_df["Date"],
        y=-market_breadth_df["Number of stocks down 4% plus"],  
        name="Stocks Down 4%", marker_color="lightcoral", opacity=0.6
    ))
    fig_breadth_up_down.update_layout(
        title="Market Breadth: 4% Up vs. 4% Down", template='plotly_dark',
        barmode='relative', height=300, margin=dict(l=40, r=40, t=40, b=40),
        yaxis_title="Number of Stocks",
        showlegend=False
    )
    charts['breadth_up_down'] = fig_breadth_up_down

    # 4b. Daily Histogram
    # fig_breadth_histogram = go.Figure()
    # for col, color in zip(["Number of stocks up 4% plus", "Number of stocks down 4% plus"],
    #                        ["lightgreen", "lightcoral"]):
    #     fig_breadth_histogram.add_trace(go.Bar(
    #         x=market_breadth_df[col],
    #         name=col, marker_color=color, opacity=0.6
    #     ))
    # fig_breadth_histogram.update_layout(
    #     title="Daily Histogram: Stocks Up and Down 4%+",
    #     template='plotly_dark', barmode='group', bargap=0.2,
    #     height=400, margin=dict(l=40, r=40, t=40, b=40),
    #     xaxis_title="Date", yaxis_title="Number of Stocks",
    #     xaxis=dict(type='category', tickformat="%Y-%m-%d"),
    #     showlegend=False
    # )
    # charts['breadth_histogram'] = fig_breadth_histogram

    return charts
