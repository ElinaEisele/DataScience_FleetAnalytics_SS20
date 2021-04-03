'''
    This python file contains the main structure of the dash layout. Underneath the header
    with the app-name, adesso logo and dash logo there is a tab bar representing the
    thematically grouped visuals.
'''

# ------------------------------------------------ index ------------------------------------------

#  Imports
import dash
import dash_core_components as dcc
import dash_html_components as html

from Dashboard.app import app
from Dashboard.panels import streamingPanel, emissionPanel, tripDriverPanel

# necessary for deployment
server = app.server

# ----------------------------------------------- layout --------------------------------------------

app.layout = html.Div(
    [
        # header
        html.Div(
            className="row header",
            children=[
                html.Div(
                    className='app-title',
                    children=[
                        html.Div(
                            className='first-titel',
                            children=[
                                dcc.Markdown("**Fleetanalytics**")
                            ]
                        ),
                        html.Div(
                            className='subtitel',
                            children=[
                                html.H2("ein HdM Projekt mit ")
                        ]),
                        html.Div(children=[
                            html.Img(src=app.get_asset_url("adesso_logo.png"),
                                    style={"float": "left"},
                            )
                        ]),
                    ],
                ),
                html.Img(src=app.get_asset_url("logo.png")),
            ],
        ),
        # tabs (linked with the corresponding page)
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Link("Emissionen", href="/"),
                dcc.Link("Fahrten & Fahrer", href="/"),
                dcc.Link("Streaming-Szenario", href="/"),
            ],
        ),
        html.Div(
            id="mobile_tabs",
            className="row tabs",
            style={"display": "none"},
            children=[
                dcc.Link("Emissionen", href="/"),
                dcc.Link("Fahrten & Fahrer", href="/"),
                dcc.Link("Streaming-Szenario", href="/"),
            ],
        ),

        # url contains the current tab
        dcc.Location(id="url", refresh=False),
        html.Div(id="tab_content"),
        html.Link(
            href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet",
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"
        ),
    ],
    className="row",
    style={"margin": "0%"},
)

# --------------------------------------------- callbacks -----------------------------------------------

@app.callback(
    [
        dash.dependencies.Output("tab_content", "children"),
        dash.dependencies.Output("tabs", "children"),
        dash.dependencies.Output("mobile_tabs", "children"),
    ],
    [dash.dependencies.Input("url", "pathname")],
)
# by clicking on the tab a new page is displayed depending on the clicked tab
def display_page(pathname):
    tabs = [
        dcc.Link("Emissionen", href="/dash-fleetanalytics-datascienceproject/emissionPanel"),
        dcc.Link("Fahrten & Fahrer", href="/dash-fleetanalytics-datascienceproject/tripDriverPanel"),
        dcc.Link("Streaming-Szenario", href="/dash-fleetanalytics-datascienceproject/streamingPanel"),
    ]
    #  depending on the set path the corresponding panel/page is returend
    if pathname == "/dash-fleetanalytics-datascienceproject/streamingPanel":
        tabs[2] = dcc.Link(
            dcc.Markdown("**&#9632 Streaming-Szenario**"),
            href="/dash-fleetanalytics-datascienceproject/streamingPanel",
        )
        return streamingPanel.layout, tabs, tabs

    elif pathname == "/dash-fleetanalytics-datascienceproject/tripDriverPanel":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Fahrten & Fahrer**"), href="/dash-fleetanalytics-datascienceproject/tripDriverPanel"
        )
        return tripDriverPanel.layout, tabs, tabs

    tabs[0] = dcc.Link(
        dcc.Markdown("**&#9632 Emissionen**"), href="/dash-fleetanalytics-datascienceproject/emissionPanel"
    )
    return emissionPanel.layout, tabs, tabs


# -------------------------------------------- run ---------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=False)