'''
    This python file represents the "Streaming Szenario" tab in the dash app. It contains the
    prediction and mockup.
'''

#  ------------------------------------- streamingPanel ------------------------------

# Imports
import dash_core_components as dcc
import dash_html_components as html
import dash
import re

from Dashboard.dashContent import predictionengine
from Dashboard.app import app

# -------------------------------------- layout ------------------------------------
layout = [
    html.Div(
        id="streamingPanel",
        children=[
            html.Div(
                id="streamingSimulation",
                className="dashElement",
                children=[
                    html.H1("Streaming Szenario mit Mockup"),
                    html.Div(
                        id="streamingContainer",
                        children=[
                            html.Button(children='Start', id='simubutton', n_clicks=0),
                            html.Button(children='↻', id='simureset', n_clicks=0),
                            html.H6(id='output', children=''),
                            dcc.Interval(
                                id='interval-component',
                                interval=1 * 1000,
                                n_intervals=0,
                                max_intervals=100,
                                disabled=False
                            ),
                            html.Img(id="behaviourimage", src='', height=350)
                        ]
                    )
                ]
            )
        ]
    )
]


# ------------------------------- callbacks --------------------------------------

# Change the Mockup Image depending on the cluster id
@app.callback(dash.dependencies.Output('behaviourimage', 'src'),
              [dash.dependencies.Input('output', 'children')])
def change_image(children):
    if children.endswith('2'):
        return 'data:image/png;base64,{}'.format(predictionengine.encode_image(predictionengine.cluster2).decode())
    if children.endswith('1'):
        return 'data:image/png;base64,{}'.format(predictionengine.encode_image(predictionengine.cluster1).decode())
    else:
        return 'data:image/png;base64,{}'.format(predictionengine.encode_image(predictionengine.cluster0).decode())


# Reset Button for the simulation
@app.callback([dash.dependencies.Output('interval-component', 'n_intervals'),
               dash.dependencies.Output('simubutton', 'n_clicks')],
              [dash.dependencies.Input('simureset', 'n_clicks')])
def reset_simulation(n_clicks):
    # Stop the simulation and reset the simubutton
    return 0, 0


# Start/Stop Button of the simulation
@app.callback([dash.dependencies.Output('output', 'children'),
               dash.dependencies.Output('interval-component', 'disabled'),
               dash.dependencies.Output('simubutton', 'children')],
              [dash.dependencies.Input('simubutton', 'n_clicks'),
               dash.dependencies.Input('interval-component', 'n_intervals')])
def auto_update(n_clicks, n_intervals):
    # Uneven number of button presses: start the simulation
    if n_clicks % 2 != 0 and n_intervals < predictionengine.length:
        # Select one row from the dataframe to simulate driving truck
        currentData = predictionengine.df_simu_fcd.iloc[n_intervals]
        speed = currentData['speed']
        acceleration = currentData['absoluteAcc']

        # Query our PredictionIO server for the result
        request = predictionengine.engine_client.asend_query({"dataPoint": [speed, acceleration]})
        try:
            response = request.get_response()
            # Only keep the number of the cluster
            cluster = re.sub('\D', '', str(response))[:1]
            return "Fahrtzeit: {} Sekunden, Geschwindigkeit: {} km/h, Beschleunigung {} m/s^2, Cluster: {}".format(
                str(n_intervals), str(round(speed, 2)), str(round(acceleration, 2)), str(cluster)), False, "Stop"
        except:
            return "Something went wrong.", True, "Start"


    # Even number of button presses: stop the simulation
    else:
        return dash.no_update, True, "Start"
