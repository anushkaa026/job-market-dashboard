import plotly.express as px

FIPS_TO_ABBR = {
    1:"AL",2:"AK",4:"AZ",5:"AR",6:"CA",8:"CO",9:"CT",10:"DE",11:"DC",
    12:"FL",13:"GA",15:"HI",16:"ID",17:"IL",18:"IN",19:"IA",20:"KS",
    21:"KY",22:"LA",23:"ME",24:"MD",25:"MA",26:"MI",27:"MN",28:"MS",
    29:"MO",30:"MT",31:"NE",32:"NV",33:"NH",34:"NJ",35:"NM",36:"NY",
    37:"NC",38:"ND",39:"OH",40:"OK",41:"OR",42:"PA",44:"RI",45:"SC",
    46:"SD",47:"TN",48:"TX",49:"UT",50:"VT",51:"VA",53:"WA",54:"WV",
    55:"WI",56:"WY"
}



REGION_COLORS = {
    "Northeast": "#e63946",
    "Midwest":   "#2a9d8f",
    "South":     "#e9c46a",
    "West":      "#457b9d",
}

def make_choropleth(df, metric_col, metric_label):
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
        points=False,
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
        color=metric_col,
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
    )

    return fig
