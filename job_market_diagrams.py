import plotly.express as px

REGION_COLORS = {
    "Northeast": "#e63946",
    "Midwest":   "#2a9d8f",
    "South":     "#e9c46a",
    "West":      "#457b9d",
}

def make_boxplot(df, metric_col, metric_label):
    df = df.dropna(subset=["region"])

    fig = px.box(
        df,
        x="region",
        y=metric_col,
        color="region",
        hover_name="state",
        color_discrete_map=REGION_COLORS,
        category_orders={"region": ["Northeast", "Midwest", "South", "West"]},
        labels={"region": "Region", metric_col: metric_label},
        title=f"{metric_label} by U.S. Region — Q2 2025",
        points=False,       # show individual state dots too
    )

    fig.update_layout(
        height=550,
        showlegend=False,
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
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
    )

    return fig
