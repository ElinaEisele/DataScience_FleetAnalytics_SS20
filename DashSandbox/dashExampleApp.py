'''
    This file contains an example Dash app and only serves testing purposes.
    Within this file we decided to experiment with Dash tables and diagrams in
    order to get a better understanding of Dash and how it works.
'''
# ------------------------------------------ dashExampleApp ---------------------------------------

# -*- coding: utf-8 -*-
# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# A static class connecting to the database. The static property ensures that there
# will be only one connection to the database for each instance of this app.
from Dashboard import databaseconnection

# Calling example data from our database with a static connection variable.
# It is recommended to add a limit to the SQL query since the table contains thousands of rows.
df = pd.read_sql('SELECT * from fleetanalytics.lkw_agg2 LIMIT 10;', con=databaseconnection.Connection.db_connection)

dfco2 = pd.read_sql('SELECT id, CO2, fuel, speed FROM fleetanalytics.lkw_emissions LIMIT 100;', con=databaseconnection.Connection.db_connection)

# Importing a local .csv file containing clustered data
# Since this file is not part of the repository, the visualization probably wont work
dfcl = pd.read_csv(filepath_or_buffer='kmeans.csv', sep=';')

# Reading the contents of a dataframe to create a dash table object
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Creating the layout for our test app
app.layout = html.Div(children=[
    html.H4(children='Daten aus AWS Datenbank'),
    generate_table(df),

    # Showing the clustered data
    html.H4(children='Sumfuel vs avg(absolute_acc)'),
    dcc.Graph(
        id='sumfuel-vs-absolute-acc',
        figure={
            'data': [
                dict(
                    x=dfcl[dfcl['label'] == i]['avg(absolute_acc)'],
                    y=dfcl[dfcl['label'] == i]['sumfuel'],
                    text=dfcl[dfcl['label'] == i]['sumfuel'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in dfcl.label.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'avg(absolute_acc)'},
                yaxis={'title': 'sumfuel'},
                margin={'l': 40, 'b': 40, 't': 20, 'r': 800},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    # First try of showing of a correlation between a cars speed and the CO2 emissions, grouped by vehicle-id
    dcc.Graph(
        id='test',
        figure={
            'data': [
                dict(
                    x=dfco2[dfco2['id'] == j]['speed'],
                    y=dfco2[dfco2['id'] == j]['CO2'],
                    text=dfco2[dfco2['id'] == j]['fuel'],
                    mode='markers',
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=j
                ) for j in dfco2.id.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'speed'},
                yaxis={'title': 'co2 emissions'},
                margin={'l': 40, 'b': 40, 't': 20, 'r': 800},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
