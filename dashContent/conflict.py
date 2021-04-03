'''
    This python file prepares a germany map with from openstreetmap and the truck accidents.
    Below is a mockup with recommendations on the driver's driving behavior
'''

# -------------------------------------------- conflict ---------------------------------------

# Imports
import base64
import pandas as pd
import plotly.express as px

# Get data from database
from Dashboard import databaseconnection

# ---------------------------------------------- prepare data --------------------------------------

# Read coordinates data from table conflicts
df_map = pd.read_sql('SELECT latitude, longitude, tripId from fleetanalytics.conflicts_coordinates',
                     con=databaseconnection.Connection.db_connection)

# -------------------------------------------- prepare dash component ---------------------------------------

# Create Scatter_Mapbox with truck accidents
fig_map = px.scatter_mapbox(df_map, hover_data=["tripId"], lat="longitude", lon="latitude",
                        color_discrete_sequence=["red"], zoom=5.5, height=800, width=800)

# Open Street Map as Map Style
fig_map.update_layout(mapbox_style="open-street-map",showlegend= True, geo_scope='europe',)
fig_map.update_layout(margin={"r":1,"t":1,"l":1,"b":1})

# Mockup image encode
image_filename = 'assets/conflictsNavi.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())