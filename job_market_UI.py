"""
UI Layer
Aspects that form the front end (our dashboard).
Dashboard goals:
Plot -- Choropleth Map & Bar Chart
Pick a state and see wage and employment data by county
- Dropdown -- state picker
- IntSlider -- top N counties (controls how many counties show in the bar chart)
- RadioButtonGroup -- metric selector (wage, employment, establishments, YoY changes)
"""

# LAYOUT

# top bar with title
# sidebar on the left with search and plot cards
    # "Search" card
        # dropdown - state picker
        # radio buttons - metric selector
    # "Plot" card
        # slider - top N counties
# main window with three tabs
    # Map tab - choropleth of all states colored by selected metric
    # Top Counties tab - bar chart of top N counties by selected metric
    # Data Table tab - state level summary table

import panel as pn
import job_market_API as api_module
import job_market_diagrams as diagrams

#Dimensions
CARD_WIDTH = 320

api = None

# Callback Functions
def get_map(metric_label):
    """Draws the choropleth map for the selected metric."""
    metric_col = api_module.METRICS[metric_label]
    df = api.get_state_summary(metric_col)
    return diagrams.make_choropleth(df, metric_col, metric_label)

def get_bar(state, metric_label, top_n):
    """Draws the bar chart for the selected state, metric, and top N."""
    metric_col = api_module.METRICS[metric_label]
    df = api.get_county_data(state=state, metric_col=metric_col, top_n=top_n)
    return diagrams.make_bar_chart(df, metric_col, metric_label, state)

def get_table(state):
    """Returns the data table filtered to the selected state."""
    df = api.get_table(state=state)
    return pn.pane.DataFrame(df, index=False)


def main():
    # Loads javascript dependencies and configures Panel (required)
    pn.extension("plotly")

    # Initialize API

    global api
    api = api_module.JobMarketAPI(api_module.DATA_FILE_PATH)

    # WIDGET DECLARATIONS
    # Search Widgets

    state_slct = pn.widgets.Select(name="State", options=api.get_states())

    metric_slct = pn.widgets.RadioButtonGroup(
        name="Metric",
        options=list(api_module.METRICS.keys()),
        value="Avg Weekly Wage ($)",
        button_type="primary",
        button_style="outline",
        orientation="vertical",
    )

    # Plotting widgets
    top_n_sldr = pn.widgets.IntSlider(name="Top N Counties", start=5, end=30, step=5, value=15)

    # CALLBACK FUNCTIONS
    # CALLBACK BINDINGS (Connecting widgets to callback functions)
    map_component   = pn.bind(get_map, metric_slct)
    bar_component   = pn.bind(get_bar, state_slct, metric_slct, top_n_sldr)
    table_component = pn.bind(get_table, state_slct)

    # Dashboard Card
    search_card = pn.Card(
        pn.Column(
            state_slct,      # dropdown - pick a state
            metric_slct,     # radio buttons - wage / employment / establishments / YoY
        ),
        title="Search", width=CARD_WIDTH, collapsed=False
    )

    plot_card = pn.Card(
        pn.Column(
            top_n_sldr,      # slider - number of counties shown in bar chart
        ),
        title="Plot", width=CARD_WIDTH, collapsed=True
    )


    layout = pn.template.FastListTemplate(
        title="U.S. Job Market Explorer — BLS Q2 2025",
        sidebar=[
            search_card,
            plot_card,
        ],
        theme_toggle=False,
        main=[
            pn.Tabs(
                ("Map",          pn.pane.Plotly(map_component)),   # choropleth map
                ("Top Counties", pn.pane.Plotly(bar_component)),   # bar chart
                ("Data Table",   table_component),                 # summary table
                active=0
            )
        ],
        header_background="#1a5276"

    ).servable()

    layout.show()

if __name__ == "__main__":
    main()