'''
    This python file develops a model to predict the CO value depending on
    a fuel value based on a linear regression between CO and fuel. Besides a
    histogram and a boxplot are created to show which trips are below and above a CO limit.
    Besides we insert the driver Ids to get a detail information.



'''

# ---------------------------- predictEmissionsDriverId -----------------------
import dash
import dash_html_components as html
import dash_table
import pandas as pd
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc


#Get data from database
from Dashboard import databaseconnection

#Get Dash App Object
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Read data
df2 = pd.read_sql(
    'SELECT COperKM, tripId, driverId from fleetanalytics.agg_driver_id WHERE COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

#Diagram to show emission data and their limits
a=df2["COperKM"]
fig2 = go.Figure(data=[go.Histogram(x=a)])

fig2 = px.histogram(df2, x="COperKM",
                   #opacity=0.8,
                   #log_y=True, # represent bars with log scale
                   color_discrete_sequence=['blue'] # color of histogram bars
                   )

#Adjust layout
fig2.update_layout(
    title="Frequency of overruning limit CO value of 2500 mg/km",
    xaxis_title="CO",
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

cond = df2['COperKM'] > 2500
df_overRedLine = df2[cond]
df = df_overRedLine['driverId'].to_frame()

df = DataFrame({'count' : df.groupby( [ "driverId"] ).size()}).reset_index()
df = df.sort_values(by=['count'], ascending=False)
df = df.rename(columns={'count':'Amount of trips with exceeded limit'})



#Dash layout
app.layout = html.Div([

    dcc.Graph(figure=fig2),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('rows'),
        style_table={
            'height': 300,
            'overflowY': 'scroll',
            'width': 800}
    )

])


if __name__ == '__main__':
    app.run_server(debug=True)
