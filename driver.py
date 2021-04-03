'''
    This python file prepares the dash figure and cluster-specific dataframes
    for the final dashapp (Vizualisation). A cluster of tree is built and depending on which
    dropdown selection a dataframe of the cluster is shown.
'''

# ----------------------------------------- driver -------------------------------------------

# Imports
import pandas as pd
from pandas import DataFrame
import plotly.express as px

# Get data from database
from Dashboard import databaseconnection

# ---------------------------------------------- prepare data --------------------------------------

# read data from table with condition that the CO per km must be less than 5000
df = pd.read_sql(
    'SELECT COperKM, tripId, driverId from fleetanalytics.agg_driver_id WHERE COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

# set condition mark for CO per km is less than 2500 and apply it to the dataframe
cond = df['COperKM'] > 2500
df_overRedLine = df[cond]
df_driver = df_overRedLine['driverId'].to_frame()

# group dataframe on the driverId and sort values by the cpount of exceeded limits
df_driver = DataFrame({'count' : df_driver.groupby( [ "driverId"] ).size()}).reset_index()
df_driver = df_driver.sort_values(by=['count'], ascending=False)
df_driver = df_driver.rename(columns={'count':'Anzahl Limit-Überschreitungen/Fahrt'})


# read cluster of drivers from dataframe
df_clusterDrivers = pd.read_sql(
    'SELECT * FROM fleetanalytics.cluster_drivers ',
    con=databaseconnection.Connection.db_connection)

# count the lanechanges per driver and rename the numerical clusters
df_clusterDrivers = df_clusterDrivers.round({'totalLanechanges':0, 'avgLanechangeSpeed':2, 'avgCO2':2, 'avgSpeed':2, 'avgAbsAcceleration':2})
df_clusterDrivers = df_clusterDrivers.rename(columns={'prediction':'Fahrergruppe'})
df_cluster = df_clusterDrivers.replace({'Fahrergruppe': {0: 'vorrausschauender Fahrer', 1: 'risikobereiter Fahrer', 2: 'langsamer Fahrer'}})
df_cluster = df_cluster.rename({'prediction':'Fahrergruppe'})

# create dataframes for each cluster
c0 = df_clusterDrivers[df_clusterDrivers['Fahrergruppe'] == 0].drop(columns=['Fahrergruppe', 'index'])
c1 = df_clusterDrivers[df_clusterDrivers['Fahrergruppe'] == 1].drop(columns=['Fahrergruppe', 'index'])
c2 = df_clusterDrivers[df_clusterDrivers['Fahrergruppe'] == 2].drop(columns=['Fahrergruppe', 'index'])

c0 = c0.rename(columns={'totalLanechanges': 'Spurwechsel', 'avgLanechangeSpeed': 'Ø Spurwechsel Geschwindigkeit', 'avgCO2': 'Ø CO2', 'avgSpeed': 'Ø Geschwindigkeit', 'avgAbsAcceleration': 'Ø Beschleunigung'})
c1 = c1.rename(columns={'totalLanechanges': 'Spurwechsel', 'avgLanechangeSpeed': 'Ø Spurwechsel Geschwindigkeit', 'avgCO2': 'Ø CO2', 'avgSpeed': 'Ø Geschwindigkeit', 'avgAbsAcceleration': 'Ø Beschleunigung'})
c2 = c2.rename(columns={'totalLanechanges': 'Spurwechsel', 'avgLanechangeSpeed': 'Ø Spurwechsel Geschwindigkeit', 'avgCO2': 'Ø CO2', 'avgSpeed': 'Ø Geschwindigkeit', 'avgAbsAcceleration': 'Ø Beschleunigung'})



# -------------------------------------------- prepare dash component ---------------------------------------

fig_clusterDrivers = px.scatter(df_cluster, x = 'avgSpeed', y = 'avgAbsAcceleration', color='Fahrergruppe', size='avgCO2',
                 hover_name="driverId", hover_data=["driverId"], color_discrete_sequence=px.colors.qualitative.T10)

text_clusterDrivers = 'Cluster zum Fahrverhalten'

# Update Layout
fig_clusterDrivers.update_layout(
    xaxis_title="Ø Geschwindigkeit in km/h",
    yaxis_title="Ø Beschleunigung",
)
