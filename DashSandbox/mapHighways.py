'''
    This python file prepares a germany map with the truck conflicts and
    lines for the german highways.
'''

# ----------------------------------------- map with highway lines -------------------------------------------

# Imports
import base64
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------- prepare data --------------------------------------

# Get data from database
from Dashboard import databaseconnection

# Read coordinates data from table conflicts
df_map = pd.read_sql('SELECT latitude, longitude, tripId from fleetanalytics.conflicts_coordinates',
                     con=databaseconnection.Connection.db_connection)

# Read coordinates from xlsx highwaysGermany
df_highways =pd.read_excel("../Dashboard/highwaysGermany.xlsx")

# -------------------------------------------- prepare dash component ---------------------------------------

# Create Scattergeo Map with conflict coordinates
fig_map = go.Figure(data=go.Scattergeo(
    lon=df_map['latitude'],
    lat=df_map['longitude'],
    text='Accident',
    mode='markers',
    marker_color='red',
    marker_size= 10,
))

# Shows the paths for german highways as a trace
highways_paths = []
for i in range(len(df_highways)):
    fig_map.add_trace(
        go.Scattergeo(
            lat = [df_highways['start_lon'][i], df_highways['end_lon'][i]],
            lon = [df_highways['start_lat'][i], df_highways['end_lat'][i]],

            # Hoverinfo with name
            hoverinfo='text',
            text=df_highways['name'][i],
            mode = 'lines',
            line = dict(width = 0.5 ,color = 'black'),
        )
    )

# Update map layout with height and scope europe
fig_map.update_layout(
    showlegend=False,
    height=700,
    geo_scope='europe',
)

# Update map land and ocean color
fig_map.update_geos(
    #px.line_geo(lon=[51.837, 51.8094], lat=[6.3556, 6.4629]),
    #center=dict(lat=48, lon=9),
    #fitbounds="locations",
    showcoastlines=True, coastlinecolor="black",
    showland=True, landcolor="lightgreen",
    showocean=True, oceancolor="lightblue",
    #projection_type = 'equirectangular',
)

# Mockup image encode
image_filename = '../Dashboard/assets/conflictsNavi.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())