'''
    This python file represents the "Emissionen" tab in the dash app. It contains the layout of th
    visuals and if there is an interaction their callbacks. The layout only contains the Div elements
    but not where or how they are placed and styled. This is part of the style.css file.
'''

# ------------------------------------------ emissionPanel -----------------------------------------

# Imports
import dash
import dash_table
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from Dashboard.dashContent import emission, donut, metadata, driver, trip
from Dashboard.app import app

# -------------------------------------- layout ------------------------------------
layout = [
    html.Div(
        id="emissionPanel",
        children=[
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
                id="linearRegressionGraph",
                className="dashElement",
                children=[
                    html.H1(children="Ausstoß Kohlenstoffmonoxid (CO)"),
                    html.Div(
                        dcc.Graph(figure=emission.fig_line)
                    ),


                ]
            ),
            html.Div(
                id='linarRegressionPrediction',
                className='dashElement',
                children=[
                    html.H1(children='Berechnung des CO Wertes bei einem bestimmten Spritverbrauch [in ml/km]:'),
                    # Table with the input fields and their labels
                    html.Div(
                        children=[
                            html.Div(
                                className='predictedCoBox',
                                children=[
                                    dcc.Input(id='inputCO', type='number', value="1")
                                ]
                            ),
                            html.Div(
                                className='predictedCoBox',
                                children=[
                                    html.H2(id='outputCO', children='Enter values')
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                id='exeededDonut',
                className='dashElement',
                children=[
                    # Percentage of overruning CO limit
                    html.H1('CO Grenzwertüberschreitungen in der Flotte in Prozent'),
                    html.H2(children='Überschreitungen in %: ' + str(round(emission.j, 2))),
                    # Idea: Donut chart to show Percentage (Number is hardcoded in donut.py file for now.)
                    dcc.Graph(figure=donut.donut),
                ]

            ),
            html.Div(
                id='exeededHist',
                className='dashElement',
                children=[
                    html.H1('Gesamtübersicht der CO Grenzwertüberschreitungen in der Flotte'),
                    html.Div(
                        className='exeededHistContainer',
                        children=[
                            dcc.Dropdown(
                                id='exceededHistDropdown',
                                className='dropdown_styles',
                                options=[
                                    {'label': 'Histogram', 'value': 'hist'},
                                    {'label': 'Boxplot', 'value': 'box'},
                                ],
                                value='hist'
                            ),
                            html.Div(id='dd-output-container-hist'),
                        ]
                    )
                ]
            ),
            html.Div(
                id='driverTable',
                className='dashElement',
                children=[
                    html.H1('Fahrer mit überschrittenen Grenzwerten'),
                    html.Div(
                        className='driverTableLimit',
                        children=[
                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in driver.df_driver.columns],
                                data=driver.df_driver.to_dict('rows'),
                                style_table={
                                    'height': 350,
                                    'overflowY': 'scroll',
                                    },
                                style_header={
                                    'position':'sticky',
                                    'top':0,
                                    'border-top': 'thin none lightgrey'
                                }
                            ),
                        ]
                    )

                ]
            ),
            html.Div(
                id='recommandationCO',
                className='dashElement',
                children=[
                    html.H1('Empfehlung zur Schadstoffreduktion: Schadstoffe reduzieren durch Verringerung des Spritverbrauchs'),
                    dcc.Graph(figure=trip.scatterfuel),
                ]
            ),
            html.Div(
                id='planTrip',
                className='dashElement',
                children=[
                    html.H1('Planung eines Trips'),
                    html.Div(
                        className='planTripContainer',
                        children=[
                            # Table with the input fields and their labels
                            html.Table(
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td("Routenlänge in km"),
                                                html.Td("Minimale Fahrtzeit in std"),
                                                html.Td("Maximale Fahrtzeit in std"),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td(dcc.Input(id='inputRouteLength', type='number', value="100", debounce=True)),
                                                html.Td(dcc.Input(id='inputEarlyArrival', type='number', value="1.2", debounce=True)),
                                                html.Td(dcc.Input(id='inputLateArrival', type='number', value="1.5", debounce=True)),

                                            ]
                                        ),
                                        html.Tr(
                                            html.Td(html.H6("Zusätzliche Metriken"))
                                        ),
                                        html.Tr(
                                            [
                                                html.Td(["Ø Beschleunigung in m/s", html.Sup("2")]),
                                                html.Td("Gesamte Wartezeit in min"),
                                                html.Td("Anzahl der Stops")
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td(dcc.Input(id='inputAcceleration', type='number', value="0.5", debounce=True)),
                                                html.Td(dcc.Input(id='inputWaitingTime', type='number', value="20", debounce=True)),
                                                html.Td(dcc.Input(id='inputWaitingCount', type='number', value="2", debounce=True))
                                            ]
                                        )
                                    ]
                                )
                            ),
                            # Text
                            html.H4(id='outputFuelPrediction', children='Enter values'),
                            dcc.Graph(id="compareRoutes"),
                        ]
                    )
                ]
            )
        ]
    )
]

# ------------------------------- callbacks --------------------------------------
# Callback for calculating CO using linear regression.
@app.callback(
    dash.dependencies.Output(component_id='outputCO', component_property='children'),
    [dash.dependencies.Input(component_id='inputCO', component_property='value')

     ])
def update_output(fuelvalue):
    try:
        # Convert user input to numpy array
        toPredict = np.array([[float(fuelvalue)]])

        # Query the trained model for the result
        result = emission.model.predict(toPredict)

        return 'Der voraussichtliche CO Wert beträgt [mg/km]: {}'.format(
            str(np.around(result[0], 2)),

        )
    except TypeError:
        return 'Der voraussichtliche Spritverbrauch beträgt [in ml/km]: '



# Callbock for the boxplot and histogram dropdown
@app.callback(
    dash.dependencies.Output('dd-output-container-hist', 'children'),
    [dash.dependencies.Input('exceededHistDropdown', 'value')])
def update_output(value):
    # dfdrop =plt.figure()
    d = emission.fig_hist
    if value == "hist":
        d = emission.fig_hist

    elif value == "box":
        d = emission.fig_box

    return dcc.Graph(figure=d)


# Callback for calculating average fuel consumption using linear regression.
@app.callback(
    [dash.dependencies.Output(component_id='outputFuelPrediction', component_property='children'),
     dash.dependencies.Output(component_id='compareRoutes', component_property='figure')],
    [dash.dependencies.Input(component_id='inputRouteLength', component_property='value'),
     dash.dependencies.Input(component_id='inputEarlyArrival', component_property='value'),
     dash.dependencies.Input(component_id='inputLateArrival', component_property='value'),
     dash.dependencies.Input(component_id='inputAcceleration', component_property='value'),
     dash.dependencies.Input(component_id='inputWaitingTime', component_property='value'),
     dash.dependencies.Input(component_id='inputWaitingCount', component_property='value')])
def update_output(inputRouteLengthValue, inputEarlyArrivalValue, inputLateArrivalValue, accelerationValue,
                  waitingTimeValue, waitingCountValue):
    try:
        speed = float(inputRouteLengthValue) / float(inputEarlyArrivalValue)
        slowerspeed = float(inputRouteLengthValue) / float(inputLateArrivalValue)
        slowerarrvialtime = float(inputRouteLengthValue) / slowerspeed
        timecost = (slowerarrvialtime - float(inputEarlyArrivalValue)) * 60

        # Convert user input to numpy array
        toPredict = np.array([[float(accelerationValue), float(speed),
                               float(waitingTimeValue), float(waitingCountValue)]])

        slowerPrediction = np.array([[float(accelerationValue), float(slowerspeed),
                                      float(waitingTimeValue), float(waitingCountValue)]])

        # Query the trained model for the result
        fuelprediction = trip.mlr.predict(toPredict)
        slowerfuelprediction = trip.mlr.predict(slowerPrediction)

        # Convert result, which is in ml/s to liters for the length of the route
        fuelprediction = round(((np.around(fuelprediction[0], 2)) * 3.6 * float(inputEarlyArrivalValue)), 2)
        slowerfuelprediction = round(((np.around(slowerfuelprediction[0], 2)) * 3.6 * float(inputEarlyArrivalValue)), 2)
        fuelsavings = fuelprediction - slowerfuelprediction

        # Compare figure
        y = [round(speed, 2), round(slowerspeed, 2)]
        compareRoutes = go.Figure()

        # Trip duration
        compareRoutes.add_trace(go.Bar(x=[float(inputEarlyArrivalValue) * 60, slowerarrvialtime * 60], y=y,
                                       orientation='h',
                                       marker_color='mediumseagreen',
                                       name="Fahrtzeit in min",
                                       ))
        # Fuel
        compareRoutes.add_trace(go.Bar(x=[-fuelprediction, -slowerfuelprediction], y=y,
                                       orientation='h',
                                       marker_color='crimson',
                                       name="Spritverbrauch in l"
                                       ))

        compareRoutes.update_layout(barmode='relative',
                                    height=300,
                                    yaxis_type='category',
                                    yaxis_title="Ø Geschwindigkeit in km/h"
                                    )

        r = html.Div(
            children=[
                html.H1('Vorhersage'),
                html.H2('Voraussichtlicher Spritverbrauch: {} Liter bei einer Ø Geschwindigkeit von: {} km/h. '
                        .format(str(fuelprediction).replace(".", ","), str(round(speed, 2)).replace(".", ","))),
                html.H2('Eine langsamere Ø Geschwindigkeit von: {} km/h reduziert den Spritverbrauch um: {} Liter & ' \
                'verlängert die Fahrtzeit um: {} Minuten.'
                        .format(str(round(slowerspeed, 2)).replace(".", ","),
                                str(round(fuelsavings, 2)).replace(".", ","), str(int(timecost))))

            ]
        )
        return r, compareRoutes

    except TypeError:
        return

    except ZeroDivisionError:
        return
