'''
    This python file develops a model to predict the CO value depending on
    a fuel value based on a linear regression between CO and fuel. Besides a
    histogram and a boxplot are created to show which trips are below and above a CO limit.


'''

# ---------------------------- predictEmission -----------------------

#Imports
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash

#Get data from database
from Dashboard import databaseconnection


#Get Dash App Object
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ---------------------------- emission: histogram -----------------------

#Read data for histogram
df2 = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)
l=len(df2.index)
i=0
for index, row in df2.iterrows():
    if row['COperKM']>2500:
        i=i+1

j=(i/l)*100

# Diagram to show emission data and their limits
a=df2["COperKM"]
fig2 = go.Figure(data=[go.Histogram(x=a)])

fig2 = px.histogram(df2, x="COperKM",
                   color_discrete_sequence=['blue'] # color of histogram bars
                   )

# Adjust layout
fig2.update_layout(
    #title="Frequency of overruning limit CO value of 2500 mg/km",
    xaxis_title="CO Austoß in mg pro Kilometer",
    yaxis_title="Frequency",
)
#Create line
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

# ---------------------------- emission: boxplot -----------------------

#Read data
df3 = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

#Create boxplot
fig3 = px.box(df3, y="COperKM")

#Create line
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

# ---------------------------- emission: line chart -----------------------

#Read data
df5 = pd.read_sql(
    'SELECT agg.avgFuel, agg.COperKM from fleetanalytics.agg '
    'LIMIT 90000;', con=databaseconnection.Connection.db_connection)

#Linear regression
x1 = df5[['avgFuel']]
y1 = df5[['COperKM']]
model1 = LinearRegression()
model1.fit(x1, y1)

# Build scatterplot
fig5 = px.scatter(df5, y="COperKM", x="avgFuel", trendline=[0,50])

#Adjust layout
fig5.update_layout(

    xaxis_title="fuel in ml/s",
    yaxis_title="CO in mg/s")

#Create line
fig5.add_trace(go.Scatter(
    x=[0,50],
    y=[100,100],
    mode="lines+markers",
    name="Limit CO value",

))

#donut diagram to show the weekly driving time of the drivers
labels = ['Fahrten mit CO-Wert unter Grenzwert', 'Fahrten mit zu hohem CO-Wert']
values = [2, 98]

donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8, textinfo="none")])

labels1 = ['Fahrten mit CO-Wert unter Grenzwert', 'Fahrten mit zu hohem CO-Wert']
values1 = [15, 85]

donut1 = go.Figure(data=[go.Pie(labels=labels1, values=values1, hole=.8, textinfo="none")])

# ---------------------------- emission: dash -----------------------

#Title
dash_text = 'Fleet Analytics Dashboard'

#Dash Layout
app.layout = html.Div([

    html.H1(
        children=[
            html.P(
                id='instructions',
                children=dash_text),
        ]
    )
    ,

#Linear regression to predict CO
html.H6(id='output', children='Enter values'),
    html.H2(children="Lineare Regression CO"),
 dcc.Graph(figure=fig5),
    html.H4(children='Berechnung des CO Wertes in ml pro Sekunde bei einem bestimmten Spritverbrauch pro Sekunde'),
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
html.H6(id='outputa', children='Enter values'),

#Overruning CO limit
html.H2(children='CO Grenzwertüberschreitungen in der Flotte'),
html.H4(children='Überschreitungen in % :'+ str(round(j,2))),
dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': 'Histogram', 'value': 'hist'},
        {'label': 'Boxplot', 'value': 'box'},
    ],
    value='hist'
),
    html.Div(id='dd-output-container5'),

])

# ---------------------------- emission: callbacks -----------------------

#dropdown histogram or boxplot
@app.callback(
    dash.dependencies.Output('dd-output-container5', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    #dfdrop =plt.figure()
    d=fig2
    if value == "hist":
        d=fig2

    elif value== "box":
        d = fig3

    return dcc.Graph(figure=d)

#dropdown driving time of drivers
@app.callback(
    dash.dependencies.Output('dd-output-container9', 'children'),
    [dash.dependencies.Input('table-dropdown1', 'value')])
def update_output(value):
    #dfdrop =plt.figure()
    d=donut
    if value == "0":
        d=donut

    elif value== "1":
        d = donut1

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


if __name__ == '__main__':
    app.run_server(debug=True)