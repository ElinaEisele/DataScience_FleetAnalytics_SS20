'''
    This python file shows an example of a dropdown list how callbacks work in dash with pyspark
'''

# --------------------------------------------- selectTables --------------------------------------

# Imports
import dash_core_components as dcc
import dash_html_components as html
from pyspark import SparkContext, SQLContext
import dash
import dash_table

# ------------------------------------------ set spark context ------------------------------------

sc = SparkContext()
sql = SQLContext(sc)

# ------------------------------------------- set variables ---------------------------------------

hostname = "database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com"
dbname = "fleetanalytics"
jdbcPort = 3306
username = "admin"
password = "fleetanalytics"

#  ------------------------------------- read sql tables as dataframe ----------------------------

df_lc = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "z_lkw_lanechanges") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load().toPandas()

df_ssm_gm = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "z_lkw_ssm_globalmeassures") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load().toPandas()

df_ssm_c = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "z_lkw_ssm_conflicts") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load().toPandas()

df = df_lc

# ------------------------------------ prepare dash -------------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='assets')
server = app.server

app.config.suppress_callback_exceptions = True
dash_text = 'Fleet Analytics Dashboard'

# --------------------------------------- build dash ------------------------------------------------

app.layout = html.Div(children=[
    html.H1(
        children=[
            html.P(
                id='instructions',
                children=dash_text),
            ]
    ),

    dcc.Dropdown(
        id='table-dropdown',
        options=[
                {'label': 'Lanechanges', 'value': 'lkw_lanechanges'},
                {'label': 'SSM Conflicts', 'value': 'lkw_ssm_conflicts'},
                {'label': 'SSM Gobalmeassures', 'value': 'lkw_ssm_globalmeassures'}
        ],
        value='lkw_lanechanges'

    ),

    html.Div(id='dd-output-container'),


])

#  -------------------------------------- callbacks -------------------------------------------------

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('table-dropdown', 'value')])
def update_output(value):
    if value == 'lkw_lanechanges':
        df = df_lc
    elif value == 'lkw_ssm_conflicts':
        df = df_ssm_c
    else:
        df = df_ssm_gm

    o =  dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df_lc.to_dict("rows"),
    )

    return o

#  ----------------------------------------------- run dash app ----------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
