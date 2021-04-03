"""
    Testfile for the development of the model to predict the average fuel, finished file can be found in the
    directory Dashboard under dashContent
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Get static database connection object
from Dashboard import databaseconnection

# Get training data from database
df = pd.read_sql(
    'SELECT tripId, waitingTime, waitingCount, avgSpeed, avgAbsAcceleration, avgFuel from fleetanalytics.agg '
    'LIMIT 1000;', con=databaseconnection.Connection.db_connection)

# Multiple linear regression to predict average fuel consumption
mlr = LinearRegression()
mlr.fit(df[['avgAbsAcceleration', 'avgSpeed', 'waitingTime', 'waitingCount']], df['avgFuel'])

# Get Dash App Object
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Build scatterplot
fig = px.scatter(df, y="avgFuel", x="avgSpeed", color="avgAbsAcceleration",
                 color_continuous_scale=px.colors.sequential.Bluyl, trendline="ols")

# Layout des Scatterplot anpassen
fig.update_layout(
    title="Mulitple Lineare Regression",
    xaxis_title="AvgSpeed",
    yaxis_title="avgFuel",
    coloraxis_colorbar=dict(
        title="AvgAbsAcceleration"
    )
)

# Dash Layout
app.layout = html.Div([
    dcc.Graph(figure=fig),
    # Header
    html.H4(children='Plan a trip'),
    # Table with the input fields and their labels
    html.Table(
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td("Route Length in km"),
                        html.Td("Minimum Travel Time in hours"),
                        html.Td("Maximum Travel Time in hours"),
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
                    html.Td(html.H6("Additional Measures"))
                ),
                html.Tr(
                    [
                        html.Td(["Average Acceleration in m/s", html.Sup("2")]),
                        html.Td("Total Waiting Time in minutes"),
                        html.Td("Number of Stops")
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
    html.H6(id='output', children='Enter values'),
    dcc.Graph(id="compareRoutes"),
])


# Callback for calculating average fuel consumption using linear regression.
@app.callback(
    [dash.dependencies.Output(component_id='output', component_property='children'),
    dash.dependencies.Output(component_id='compareRoutes', component_property='figure')],
    [dash.dependencies.Input(component_id='inputRouteLength', component_property='value'),
     dash.dependencies.Input(component_id='inputEarlyArrival', component_property='value'),
     dash.dependencies.Input(component_id='inputLateArrival', component_property='value'),
     dash.dependencies.Input(component_id='inputAcceleration', component_property='value'),
     dash.dependencies.Input(component_id='inputWaitingTime', component_property='value'),
     dash.dependencies.Input(component_id='inputWaitingCount', component_property='value')])
def update_output(inputRouteLengthValue, inputEarlyArrivalValue, inputLateArrivalValue, accelerationValue, waitingTimeValue, waitingCountValue):
    try:
        speed = float(inputRouteLengthValue) / float(inputEarlyArrivalValue)
        slowerspeed = float(inputRouteLengthValue) / float(inputLateArrivalValue)
        slowerarrvialtime =float(inputRouteLengthValue)/slowerspeed
        timecost = (slowerarrvialtime - float(inputEarlyArrivalValue)) * 60

        # Convert user input to numpy array
        toPredict = np.array([[float(accelerationValue), float(speed),
                               float(waitingTimeValue), float(waitingCountValue)]])

        slowerPrediction = np.array([[float(accelerationValue), float(slowerspeed),
                               float(waitingTimeValue), float(waitingCountValue)]])

        # Query the trained model for the result
        fuelprediction = mlr.predict(toPredict)
        slowerfuelprediction = mlr.predict(slowerPrediction)

        # Convert result, which is in ml/s to liters for the length of the route
        fuelprediction = round(((np.around(fuelprediction[0], 2)) * 3.6 * float(inputEarlyArrivalValue)), 2)
        slowerfuelprediction = round(((np.around(slowerfuelprediction[0], 2)) * 3.6 * float(inputEarlyArrivalValue)), 2)
        fuelsavings = fuelprediction - slowerfuelprediction

        #------------------------------------Compare Figure--------------------------------------------
        y = [round(speed,2), round(slowerspeed,2)]
        compareRoutes = go.Figure()
        # Fahrtdauer
        compareRoutes.add_trace(go.Bar(x=[float(inputEarlyArrivalValue)*60, slowerarrvialtime*60], y=y,
                                    orientation='h',
                                    marker_color='mediumseagreen',
                                    name="Travel Time in Minutes",
                                    ))
        # Fuel
        compareRoutes.add_trace(go.Bar(x=[-fuelprediction, -slowerfuelprediction], y=y,
                                    orientation='h',
                                    marker_color='crimson',
                                    name="Fuel consumption in liters"
                                    ))


        compareRoutes.update_layout(barmode='relative', title_text='Compare Fastest and Slowest drive',
                                 height=300,
                                 yaxis_type='category',
                                 yaxis_title="Average Speed in km/h"
                                 )

        return ('The predicted total fuel consumption is {} liters with an average recommended speed of {} km/h. ' \
               'Driving with a slower average speed of {} km/h would reduce the fuel consumption by {} liters while ' \
               'increasing travel time by {} minutes.'.format(
            str(fuelprediction).replace(".", ","), str(round(speed, 2)).replace(".", ","),
            str(round(slowerspeed, 2)).replace(".", ","), str(round(fuelsavings, 2)).replace(".", ","),
            str(int(timecost))), compareRoutes

        )
    except TypeError:
        return

    except ZeroDivisionError:
        return


if __name__ == '__main__':
    app.run_server(debug=True)


