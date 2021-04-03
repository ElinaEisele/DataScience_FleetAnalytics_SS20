'''
    This python file prepares a test map with the conflict coordinates
'''

# -------------------------------------------- Test Map ---------------------------------------

# Imports
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------- prepare data --------------------------------------

# Get Dash App Object
from BastDataPreparation import databaseconnection

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_sql('SELECT latitude, longitude, tripId from fleetanalytics.conflicts_coordinates', con=databaseconnection.Connection.db_connection)


# -------------------------------------------- prepare dash component ---------------------------------------

fig = px.scatter_mapbox(df, hover_data=["tripId"], lat="longitude", lon="latitude",
                        color_discrete_sequence=["red"], zoom=5.5, height=900, width=900)
fig.update_layout(mapbox_style="open-street-map",showlegend= True, geo_scope='europe',)
fig.update_layout(margin={"r":1,"t":1,"l":1,"b":1})


app.layout = html.Div([
    dcc.Graph(figure=fig),
    # Header
    html.H4(children='Test OSM')
])


if __name__ == '__main__':
    app.run_server(debug=True)
