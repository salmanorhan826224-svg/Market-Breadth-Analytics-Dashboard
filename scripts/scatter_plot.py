
import os
import pandas as pd
import plotly.graph_objects as go

def create_scatter_plot(percent_above_below_file, scatter_plot_file):
    """
    Creates a Plotly scatter plot for % Above/Below 200-Day MA.
    """
    print("\n==> [8] Creating Scatter Plot: % Above/Below 200-Day MA...")
    df_200 = pd.read_excel(percent_above_below_file) if os.path.exists(percent_above_below_file) else pd.DataFrame()
    if df_200.empty:
        print("[8] Scatter plot data is empty.")
    else:
      
        df_200.sort_values("percent_above_below", ascending=False, inplace=True)
       
        top20_200 = df_200.head(20).index
        df_200["label"] = ""
        df_200.loc[top20_200, "label"] = df_200["stock"]
    
        scatter_fig = go.Figure()
        scatter_fig.add_trace(
            go.Scatter(
                x=df_200.index,
                y=df_200["percent_above_below"],
                mode='markers+text',
                marker=dict(
                    size=df_200["last_price"]/10, 
                    color=df_200["percent_above_below"],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=df_200["label"],
                textposition='top center',
                hovertext=df_200[["stock", "last_price", "percent_above_below"]].apply(
                    lambda row: f"Stock: {row['stock']}<br>"
                                f"Last Price: {row['last_price']:.2f}<br>"
                                f"% Above/Below 200 MA: {row['percent_above_below']:.2f}%",
                    axis=1
                ),
                name="% Above/Below 200 MA"
            )
        )
    
        scatter_fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='black',
            plot_bgcolor='black',
            title={
                "text": "Stock Performance vs. 200-Day Moving Average",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 20, "color": "white"}
            },
            xaxis_title='Stocks (sorted by % above 200 MA)',
            yaxis_title='% Above/Below 200 MA',
            showlegend=False,
            height=300,
            width=800
        )
    
        scatter_fig.update_traces(textfont=dict(color='white'))
        scatter_fig.update_xaxes(tickfont=dict(color='white'), showgrid=True, gridcolor='gray')
        scatter_fig.update_yaxes(tickfont=dict(color='white'), showgrid=True, gridcolor='gray')
    
        # Save to HTML
        scatter_html = scatter_fig.to_html(full_html=False, include_plotlyjs='cdn')
        with open(scatter_plot_file, "w", encoding="utf-8") as f:
            f.write(scatter_html)
        print(f"[8] Scatter plot saved to: {scatter_plot_file}")
