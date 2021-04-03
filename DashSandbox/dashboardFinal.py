'''
    This file contains all dash elements which should be placed in the final dashboard.
    The elements are collected in here but not yet styled or put in the right order.
'''

# ------------------------------------------ dashboardFinal ---------------------------------------

# Imports
import base64

import dash_table
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash

# Get data from database
from Dashboard import databaseconnection

# Get Dash App Object
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# -----------------------------------------Emily: Emissions-------------------------------------------------

# read data for the histogram
df2 = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)
l = len(df2.index)
i = 0
for index, row in df2.iterrows():
    if row['COperKM'] > 2500:
        i = i + 1

j = (i / l) * 100
# Diagram to show emission data and their limits
a = df2["COperKM"]
fig2 = go.Figure(data=[go.Histogram(x=a)])

fig2 = px.histogram(df2, x="COperKM",
                    color_discrete_sequence=['seagreen']  # color of histogram bars
                    )

# update histogram layout
fig2.update_layout(
    # title="Frequency of overruning limit CO value of 2500 mg/km",
    xaxis_title="CO Austoß in mg pro Kilometer",
    yaxis_title="Frequency",
)
# create line
fig2.add_shape(
    dict(
        type="line",
        x0=2500,
        y0=0,
        x1=2500,
        y1=160,
        line=dict(
            color="red",
            width=3

        )
    )
)
# read data
df3 = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

# create boxplot
fig3 = px.box(df3, y="COperKM",color_discrete_sequence=['seagreen'] )

# create line in boxplot
fig3.add_shape(
    dict(
        type="line",
        x0=-1,
        y0=2500,
        x1=1,
        y1=2500,
        line=dict(
            color="red",
            width=3

        )
    )
)

fig3.update_layout(
    yaxis_title="CO Austoß in mg pro Kilometer")

# read data
df5 = pd.read_sql(
    'SELECT emissions.fuel, emissions.CO from fleetanalytics.emissions '
    'LIMIT 90000;', con=databaseconnection.Connection.db_connection)

# linear regression to predict NOx
x1 = df5[['fuel']]
y1 = df5[['CO']]
model1 = LinearRegression()
model1.fit(x1, y1)

# Build scatterplot
fig5 = px.line(df5, y="CO", x="fuel",color_discrete_sequence=['seagreen'] )

# adapt layout of the scatterplot
fig5.update_layout(

    xaxis_title="fuel in ml/s",
    yaxis_title="CO in mg/s")

# line
fig5.add_trace(go.Scatter(
    x=[0, 50],
    y=[100, 100],
    mode="lines+markers",
    name="Limit CO value",

))

# -----------------------------------------Michael: Predict Fuel--------------------------------------------------
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
scatterfuel = px.scatter(df, y="avgFuel", x="avgSpeed", color="avgAbsAcceleration",
                         color_continuous_scale=px.colors.sequential.Bluyl, trendline="ols")

# Layout des Scatterplot anpassen
scatterfuel.update_layout(
    title="Mulitple Lineare Regression",
    xaxis_title="AvgSpeed",
    yaxis_title="avgFuel",
    coloraxis_colorbar=dict(
        title="AvgAbsAcceleration"
    )
)

# -----------------------------------------Ines: Map--------------------------------------------------
df4 = pd.read_sql('SELECT latitude, longitude, tripId from fleetanalytics.conflicts_coordinates',
                  con=databaseconnection.Connection.db_connection)


fig4 = go.Figure(data=go.Scattergeo(
    lon=df4['latitude'],
    lat=df4['longitude'],
    text='Accident',
    mode='markers',
    marker_color='red',
))

fig4.update_layout(
    height=800,
    #title='Truck accidents in germany<br>(Hover for coordinates)',
    geo_scope='europe',
)

fig4.update_geos(
    # center=dict(lon=-10, lat=54),
    # showcoastlines=True, coastlinecolor="black",
    showland=True, landcolor="green",
    showocean=True, oceancolor="lightblue",
)

image_filename ='Conflicts_Navi.png'
# replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# -------------------------------------- Elina Cluster ----------------------------------------------------------

#  read data
df5 = pd.read_sql(
    'SELECT COperKM, tripId, driverId from fleetanalytics.agg_driver_id WHERE COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

# select data by condition
cond = df5['COperKM'] > 2500
df_overRedLine = df5[cond]
df6 = df_overRedLine['driverId'].to_frame()

# summarize count of exceeded limits
df6 = DataFrame({'count' : df6.groupby( [ "driverId"] ).size()}).reset_index()
df6 = df6.sort_values(by=['count'], ascending=False)
df6 = df6.rename(columns={'count':'Amount of trips with exceeded limit'})

#  read cluster data
df7 = pd.read_sql(
    'SELECT * FROM fleetanalytics.cluster_drivers ',
    con=databaseconnection.Connection.db_connection)

# round and rename data
df7 = df7.round({'totalLanechanges':0, 'avgLanechangesSpeed':2, 'avgCO2':2, 'avgSpeed':2, 'avgAbsAcceleration':2})
df8 = df7.replace({'prediction': {0: 'vorrausschauender Fahrer', 1: 'risikobereiter Fahrer', 2: 'langsamer Fahrer'}})
df8 = df8.rename({'prediction':'Fahrergruppe'})

# create dataframes for each cluster
c0 = df7[df7['prediction'] == 0].drop(columns=['prediction', 'index'])
c1 = df7[df7['prediction'] == 1].drop(columns=['prediction', 'index'])
c2 = df7[df7['prediction'] == 2].drop(columns=['prediction', 'index'])

# create scatterplot
fig9 = px.scatter(df8, x = 'avgSpeed', y = 'avgAbsAcceleration', color='prediction', size='avgCO2',
                 hover_name="driverId", hover_data=["driverId"])

text10 = 'Cluster zum Fahrverhalten'

# -----------------------------------------Layout Dash App--------------------------------------------------------

dash_text = 'Fleet Analytics Dashboard'
# Dash Layout
app.layout = html.Div([

    html.H1(
        children=[
            html.P(
                id='instructions',
                children=dash_text),
        ]
    ),
    # --------------------------------------Predict Emissions ------------------------------------------------------
    html.H2(children="Lineare Regression CO"),
    dcc.Graph(figure=fig5),
    # Header
    html.H4(children='Berechnung des CO Wertes in ml pro Sekunde bei einem bestimmten Spritverbrauch pro Sekunde'),
    # Table with the input fields and their labels
    html.Table(
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(["fuel in ml/s"]),
                    ]
                ),
                html.Tr(
                    [
                        html.Td(dcc.Input(id='inputCO', type='number', value="1"))

                    ]
                )
            ]
        )
    ),
    html.H4(id='outputa', children='Enter values'),

    html.H2(children='CO Grenzwertüberschreitungen in der Flotte'),
    html.H4(children='Überschreitungen in % :' + str(round(j, 2))),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Histogram', 'value': 'hist'},
            {'label': 'Boxplot', 'value': 'box'},
        ],
        value='hist'
    ),
    html.Div(id='dd-output-container5'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df6.columns],
        data=df6.to_dict('rows'),
        style_table={
            'height': 300,
            'overflowY': 'scroll',
            'width': 700}
    ),

    html.H4(children='Empfehlung: Schadstoffe reduzieren durch Verringerung des Spritverbrauchs'),

    # ----------------------------------------------Predict Fuel-----------------------------------------------------

    dcc.Graph(figure=scatterfuel),
    # Header
    html.H2(children='Plan a trip'),
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
    html.H4(id='outputFuelPrediction', children='Enter values'),
    dcc.Graph(id="compareRoutes"),

    # ------------------ Cluster Drivers
    html.H2(children=text10),
    dcc.Graph(figure=fig9),

    dcc.Dropdown(
        id='table-dropdown',
        options=[
                {'label': 'vorrausschauender Fahrer', 'value': 0},
                {'label': 'risikobereiter Fahrer', 'value': 1},
                {'label': 'langsamer Fahrer', 'value': 2}
        ],
        value=0

    ),

    html.Div(id='dd-output-container6'),

    html.H2(children="Flottenunfälle in Deutschland"),
    html.Div([
    dcc.Graph(figure=fig4),

    html.H4(children="Mock Up zur Warnung vor kritischen Stellen auf der Flottenroute"),
    html.H6(children="Mit Empfehlung zum Fahrverhalten"),
    html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height=350)
])

])

])


# -------------------------- Callbacks ------------------------------------------

@app.callback(
    dash.dependencies.Output('dd-output-container5', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    d = fig2
    if value == "hist":
        d = fig2

    elif value == "box":
        d = fig3

    return dcc.Graph(figure=d)


# Callback for calculating average fuel consumption using linear regression.
@app.callback(
    dash.dependencies.Output(component_id='outputa', component_property='children'),
    [dash.dependencies.Input(component_id='inputCO', component_property='value')

     ])
def update_output(fuelvalue):
    try:
        # Convert user input to numpy array
        toPredict = np.array([[float(fuelvalue)]])

        # Query the trained model for the result
        result = model1.predict(toPredict)

        return 'The predicted CO value is [in m/s]: {}'.format(
            str(np.around(result[0], 2)),

        )
    except TypeError:
        return 'The predicted average fuel consumption is [in m/s]: '


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
        fuelprediction = mlr.predict(toPredict)
        slowerfuelprediction = mlr.predict(slowerPrediction)

        # Convert result, which is in ml/s to liters for the length of the route
        fuelprediction = round(((np.around(fuelprediction[0], 2)) * 3.6 * float(inputEarlyArrivalValue)), 2)
        slowerfuelprediction = round(((np.around(slowerfuelprediction[0], 2)) * 3.6 * float(inputEarlyArrivalValue)), 2)
        fuelsavings = fuelprediction - slowerfuelprediction

        # ------------------------------------Compare Figure--------------------------------------------
        y = [round(speed, 2), round(slowerspeed, 2)]
        compareRoutes = go.Figure()
        # Fahrtdauer
        compareRoutes.add_trace(go.Bar(x=[float(inputEarlyArrivalValue) * 60, slowerarrvialtime * 60], y=y,
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


@app.callback(
    dash.dependencies.Output('dd-output-container6', 'children'),
    [dash.dependencies.Input('table-dropdown', 'value')])
def update_output(value):
    if value == 0:
        df = c0
    elif value == 1:
        df = c1
    else:
        df = c2
    t = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'height': 300,
            'overflowY': 'scroll'
        }
    )

    return t

# --------------------------------------------------- run ------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
