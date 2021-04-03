'''
    This python file represents the "Fahrer und Fahrten" tab in the dash app. It contains the
    layout of the visuals and if there is an interaction their callbacks. The layout only contains
    the Div elements but not where or how they are placed and styled. This is part of the style.css file.
'''

# --------------------------------------- tripDriverPanel -------------------------------

# Imports
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash

from Dashboard.dashContent import trip, driver, metadata, emission, donut, conflict
from Dashboard.app import app
from Dashboard.dashContent.conflict import encoded_image

# -------------------------------------------- layout -------------------------------------

layout = [
    html.Div(
        id='tripDriverPanel',
        children=[
            html.Div(
                id="driverBehaviourCluster",
                className="dashElement dashHeadings",
                children=[
                    html.H1('Cluster zum Fahrverhalten'),
                    html.Div(
                        children=[
                            dcc.Graph(figure=driver.fig_clusterDrivers)
                        ]
                    )
                ]
            ),
            html.Div(
                id="metaDataContainer",
                children=[
                    html.Div(
                        className="metaElement",
                        children=[
                            html.Span(metadata.driverCountTitle, className="metaDataDesc"),
                            html.Div(
                                className="metaDataIconContainer",
                                children=[
                                    html.Img(src="https://image.flaticon.com/icons/svg/1532/1532082.svg",
                                             className="driverIcon"),
                                    html.Span(metadata.driverCount, className="metaDataKPI")
                                ]
                            ),
                            html.Span(metadata.driverCountUnit, className="metaDataDesc")
                        ]
                    ),
                    html.Div(
                        className="metaElement",
                        children=[
                            html.Span("Ø Dieselverbrauch der Flotte", className="metaDataDesc"),
                            html.Div(
                                className="metaDataIconContainer",
                                children=[
                                    html.Img(src="https://image.flaticon.com/icons/svg/2933/2933839.svg",
                                             className="driverIcon"),
                                    html.Span(metadata.fleetAverageFuel, className="kennZahl"),
                                ],
                            ),
                            html.Span("Liter/km", className="metaDataDesc")
                        ]
                    ),
                    html.Div(
                        className="metaElement",
                        children=[
                            html.Span("Ø Strecke pro Fahrer", className="metaDataDesc"),
                            html.Div(
                                className="metaDataIconContainer",
                                children=[
                                    html.Img(src="https://image.flaticon.com/icons/svg/2164/2164589.svg",
                                             className="driverIcon"),
                                    html.Span(metadata.averageDrivingDistance, className="kennZahl"),
                                ]
                            ),
                            html.Span("km", className="metaDataDesc")
                        ]
                    )
                ]
            ),
            html.Div(
                id="occupancyRate",
                className="dashElement",
                children=[
                    html.H1("Auslastungsgrad"),
                    html.Div(
                        className="occupancyRateContainer",
                        children=[
                            dcc.Dropdown(
                                id='occupancyRate-dropdown',
                                className="dropdown_styles",
                                options=[
                                    {'label': 'Fahrer 1', 'value': '0'},
                                    {'label': 'Fahrer 2', 'value': '1'},
                                    {'label': 'Fahrer 3', 'value': '2'},
                                    {'label': 'Fahrer 4', 'value': '3'},
                                    {'label': 'Fahrer 5', 'value': '4'},
                                    {'label': 'Fahrer 6', 'value': '5'},
                                    {'label': 'Fahrer 7', 'value': '6'},
                                    {'label': 'Fahrer 8', 'value': '7'},
                                    {'label': 'Fahrer 9', 'value': '8'},
                                    {'label': 'Fahrer 10', 'value': '9'},
                                    {'label': 'Fahrer 11', 'value': '10'},
                                ],
                                value=0
                            ),
                            html.Div(id='dd-output-driverOccupancy'),
                        ]
                    ),
                ]
            ),
            html.Div(
                id="driverGroup",
                className="dashElement",
                children=[
                    html.H1('Fahrergruppen'),
                    html.Div(
                        className="driverGroupContainer",
                        children=[
                            # Dropdown to select boxplot or histogram
                            dcc.Dropdown(
                                id='driverGroup-dropdown',
                                className="dropdown_styles",
                                options=[
                                    {'label': 'vorrausschauender Fahrer', 'value': 0},
                                    {'label': 'risikobereiter Fahrer', 'value': 1},
                                    {'label': 'langsamer Fahrer', 'value': 2}
                                ],
                                value=0
                            ),
                            html.Br(),
                            html.Div(id='dd-output-container-driverGroup')
                        ]
                    )
                ]
            ),
            html.Div(
                id="warningMockup",
                className="dashElement",
                children=[
                    html.H1('Mock Up zur Warnung vor kritischen Stellen auf der Route'),
                    html.H2('mit Empfehlung zum Fahrverhalten'),
                    # Mockup to warn the driver
                    html.Div(
                        className='warningMockupContainer',
                        children=[
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), className='warningMockupImg')
                        ]
                    )
                ]
            ),
            html.Div(
                id="accidentMap",
                className="dashElement",
                children=[
                    html.H1('Flottenunfälle in Deutschland'),
                    html.Div(
                        className='mapContainer',
                        children=[
                            dcc.Graph(figure=conflict.fig_map),
                        ]
                    )
                ]
            )
        ]
    )
]

# ------------------------------- callbacks --------------------------------------

# Callbock for the boxplot and histogram dropdown
@app.callback(
    dash.dependencies.Output('dd-output-container-driverGroup', 'children'),
    [dash.dependencies.Input('driverGroup-dropdown', 'value')])
def update_output(value):
    if value == 0:
        df = driver.c0
    elif value == 1:
        df = driver.c1
    else:
        df = driver.c2
    t = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'height': 250,
            'overflowY': 'scroll'
        },
        style_header={
            'position':'sticky',
            'top':0,
            'border-top': 'thin none lightgrey'
        }
    )

    return t

#Callback for the donut diagramm
@app.callback(
    dash.dependencies.Output('dd-output-driverOccupancy', 'children'),
    [dash.dependencies.Input('occupancyRate-dropdown', 'value')])
def update_output(value):
    notExceeded = 'Die tägliche Lenkzeit von maximal 9h wurde nicht überschritten.'
    exeeded = 'Die tägliche Lenkzeit von maximal 9h wurde zweimal überschritten:'
    d= donut.donut1
    e= 'Die tägliche Lenkzeit von maximal 9h wurde nicht überschritten.'

    if value == "0":
        d= donut.donut1
        e= notExceeded
    elif value== "1":
        d = donut.donut2
        e = notExceeded
    elif value== "2":
        d = donut.donut3
        e = notExceeded
    elif value== "3":
        d = donut.donut4
        e = notExceeded
    elif value== "4":
        d = donut.donut5
        e = 'Die tägliche Lenkzeit von maximal 9h wurde zweimal überschritten: 20.5.2020: 9.5h; 27.5.2020: 10h'
    elif value== "5":
        d = donut.donut6
        e = notExceeded
    elif value== "6":
        d = donut.donut7
        e = notExceeded
    elif value== "7":
        d = donut.donut8
        e = notExceeded
    elif value == "8":
        d = donut.donut9
        e = notExceeded
    elif value == "9":
        d = donut.donut10
        e = notExceeded
    elif value == "10":
        d = donut.donut11
        e = notExceeded
    return dcc.Graph(figure=d), e