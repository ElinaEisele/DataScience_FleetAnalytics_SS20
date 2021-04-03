'''
    This python file prepares a scatterplot for the truck conflicts in a (germany) map
'''

#------------------------------ ScatterPlot on a  Map -------------------------------

# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------- prepare data -----------------------------------

# Get Dash App Object
from Dashboard import databaseconnection

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_sql('SELECT latitude, longitude, tripId from fleetanalytics.conflicts_coordinates', con=databaseconnection.Connection.db_connection)

# Print the first 100 rows of the table for testing
print(df.head(100))

# -------------------------------------------- prepare dash component ---------------------------------------

fig = go.Figure(data=go.Scattergeo(
        lon=df['latitude'],
        lat = df['longitude'],
        text = 'Accident',
        mode = 'markers',
        marker_color = 'red',
        ))

fig.update_layout(
        height=800,
        title = 'Truck accidents in germany<br>(Hover for coordinates)',
        geo_scope='europe',
    )

fig.update_geos(
    #center=dict(lon=-10, lat=54),
    #showcoastlines=True, coastlinecolor="black",
    showland=True, landcolor="lightblue",
    showocean=True, oceancolor="grey",
)

app.layout = html.Div([
    dcc.Graph(figure=fig),

])


if __name__ == '__main__':
    app.run_server(debug=True)
