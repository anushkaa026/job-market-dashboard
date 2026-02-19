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

def make_bar_chart(df, metric_col, metric_label, state):
    """
    Builds a horizontal bar chart of the top counties by the selected metric.
    """
    title = f"Top Counties by {metric_label}"
    if state != "All States":
        title += f" — {state}"

    fig = px.bar(
        df,
        x=metric_col,
        y="county_label",
        orientation="h",
        title=title,
        labels={metric_col: metric_label, "county_label": "County FIPS"},
        color=metric_col,
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
    )

    return fig
