'''
    This python file prepares a Scattergeo Map with the conflict coordinates and the truck trips
'''

# -------------------------------------------- trips_OnMap ---------------------------------------

# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


# Get Dash App Object
from Dashboard import databaseconnection

# ---------------------------------------------- prepare data --------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_sql('SELECT latitude, longitude, tripId from fleetanalytics.conflicts_coordinates', con=databaseconnection.Connection.db_connection)

df_trip_paths = pd.read_sql('SELECT * FROM fleetanalytics.coordiantes', con=databaseconnection.Connection.db_connection)
#df_trip_paths.head()

# -------------------------------------------- prepare dash component ---------------------------------------
fig = go.Figure()

#Coordinates for conflicts
fig.add_trace(go.Scattergeo(
        lon=df['latitude'],
        lat = df['longitude'],
        text = 'Accident',
        mode = 'markers',
        marker_color = 'red',
        ))


trip_paths = []
for i in range(len(df_trip_paths)):
    fig.add_trace(
        go.Scattergeo(
            #locationmode = 'europe',
            lat = [df_trip_paths['startLongitude'][i], df_trip_paths['endLongitude'][i]],
            lon = [df_trip_paths['startLatitude'][i], df_trip_paths['endLatitude'][i]],
            mode = 'lines',
            #hoverinfo = 'text',
            #text = df_trip_paths['tripId'],
            line = dict(width = 2,color = 'orange'),
        )
    )

fig.update_layout(
    height=800,
    #title_text = 'Truck trips in Germany<br>(Hover for trip information)',
    showlegend = False,
    geo = dict(
        scope = 'europe',
        #projection_type = 'azimuthal equal area',
        #showland = True,
        showland=True, landcolor="lightblue",
        showocean=True, oceancolor="grey",
    ),
)



app.layout = html.Div([
    dcc.Graph(figure=fig),


])

if __name__ == '__main__':
    app.run_server(debug=True)
