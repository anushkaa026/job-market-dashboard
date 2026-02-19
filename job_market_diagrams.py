import plotly.express as px


def make_choropleth(df, metric_col, metric_label):
    """
    Builds a filled U.S. state map colored by the selected metric.
    """
    
    fig = px.choropleth(
        df,
        locations="state_fips",
        locationmode="USA-states",
        color=metric_col,
        scope="usa",
        hover_name="state",
        color_continuous_scale="Blues",
        labels={metric_col: metric_label},
        title=f"{metric_label} by State — Q2 2025",
    )
    return fig
