'''
    This python file reads an already labeld dataframe and implements a dash visualization
    for this dataframe.
'''

# ------------------------------------------- clusterDrivingProfiles ----------------------------------

# Imports
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_table
import plotly.express as px
import pandas as pd

# Get static database connection object
from Dashboard import databaseconnection

# ------------------------------------ get data from database ------------------------------------------

cluster_df = pd.read_sql(
    'SELECT * FROM fleetanalytics.cluster_drivers ',
    con=databaseconnection.Connection.db_connection)

# rename numerical clusters
cluster_df_rn = cluster_df.replace({'prediction': {0: 'vorrausschauender Fahrer', 1: 'risikobereiter Fahrer', 2: 'langsamer Fahrer'}})
cluster_df_rn = cluster_df_rn.rename({'prediction':'Fahrergruppe'})

#  create 3 dataframes for each cluster
c0 = cluster_df[cluster_df['prediction'] == 0].drop(columns=['prediction', 'index'])
c1 = cluster_df[cluster_df['prediction'] == 1].drop(columns=['prediction', 'index'])
c2 = cluster_df[cluster_df['prediction'] == 2].drop(columns=['prediction', 'index'])


# ---------------------------------------- prepare charts ----------------------------------------------------

fig = px.scatter(cluster_df_rn, x = 'avgSpeed', y = 'avgAbsAcceleration', color='prediction', size='avgCO2',
                 hover_name="driverId", hover_data=["driverId"])


# ---------------------------------------- prepare dash ------------------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='assets')
server = app.server

app.config.suppress_callback_exceptions = True
dash_text = 'Fleet Analytics Dashboard'
dash_chart = 'Cluster zum Fahrverhalten mit Daten aus der cluster_driver Tabelle'

# ----------------------------------------- build dash ------------------------------------------------------

app.layout = html.Div(children=[
    html.H1(
        children=[
            html.P(
                id='instructions',
                children=dash_text),
            ]
    ),

    html.H2(children=dash_chart),
    dcc.Graph(figure=fig),

    dcc.Dropdown(
        id='table-dropdown',
        options=[
                {'label': 'vorrausschauender Fahrer', 'value': 0},
                {'label': 'risikobereiter Fahrer', 'value': 1},
                {'label': 'langsamer Fahrer', 'value': 2}
        ],
        value=0

    ),

    html.Div(id='dd-output-container')

])

# ------------------------------------ callbacks -------------------------------------------------------

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
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


#  ----------------------------------------- run dash app ------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)


