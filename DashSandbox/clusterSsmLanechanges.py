'''
    This python file explores the lanechanges and ssm data by developing a cluster on these
    datasets concerning the driovers behavior in accident situations.
'''

# ------------------------------------- clusterSsmLanechanges ---------------------------------------

# Imports
import dash_core_components as dcc
import dash_html_components as html
import dash
import plotly.express as px
import pandas as pd

# Get static database connection object
from Dashboard import databaseconnection

# ---------------------------------------------- get data from database ------------------------------------------

# read the prepared table from database based on 5 clusters
cluster_df = pd.read_sql(
    'SELECT * FROM fleetanalytics.ssm_lc_cluster_tripId_oAk5 ',
    con=databaseconnection.Connection.db_connection)

# read a mapping table with the columns tripId and driverId
driver_df = pd.read_sql(
    'SELECT * FROM fleetanalytics.trip_driver_id ',
    con=databaseconnection.Connection.db_connection)

# join the driverId to the cluster dataframe
cluster_driver_df = pd.merge(cluster_df, driver_df, left_index=True,  on='tripId', how='left')

# print(cluster_driver_df)

# ------------------------------------- prepare charts --------------------------------------------

fig = px.scatter(cluster_driver_df, x = 'medianSpeed', y = 'medianOrigLeaderGap', color='prediction', size='medianMinSgapValue')


# -------------------------------------- prepare dash ---------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='assets')
server = app.server

app.config.suppress_callback_exceptions = True
dash_text = 'Fleet Analytics Dashboard'
dash_chart = 'Cluster zum Fahrverhalten bei Fahrten mit Unfällen'


# --------------------------------- build dashboard ------------------------------------

app.layout = html.Div(children=[
    html.H1(
        children=[
            html.P(
                id='instructions',
                children=dash_text),
            ]
    ),

    html.H2(children=dash_chart),
    dcc.Graph(figure= fig),
])

#  ----------------------------------------- run dash app -----------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
