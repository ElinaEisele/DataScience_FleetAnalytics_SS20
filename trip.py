"""
    Model and Scatterplot used to predict the fuel usage
"""

# Imports
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
import dash

# Get data from database
from Dashboard import databaseconnection

# Read data from fleetanalytics.agg
df_trips = pd.read_sql(
    'SELECT tripId, waitingTime, waitingCount, avgSpeed, avgAbsAcceleration, avgFuel from fleetanalytics.agg '
    'LIMIT 1000;', con=databaseconnection.Connection.db_connection)

# Multiple linear regression to predict average fuel consumption
mlr = LinearRegression()
mlr.fit(df_trips[['avgAbsAcceleration', 'avgSpeed', 'waitingTime', 'waitingCount']], df_trips['avgFuel'])

# Get Dash App Object
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Build scatterplot
scatterfuel = px.scatter(df_trips, y="avgFuel", x="avgSpeed", color="avgAbsAcceleration",
                         color_continuous_scale=px.colors.sequential.Bluyl, trendline="ols")

# Update Layout
scatterfuel.update_layout(
    xaxis_title="Ø Geschwindigkeit in km/h",
    yaxis_title="Ø Spritverbrauch in Liter",
    coloraxis_colorbar=dict(
        title="Ø Beschleunigung"
    )
)