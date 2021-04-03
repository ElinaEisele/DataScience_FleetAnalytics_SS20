'''
    This python file is part of the Data Preperation for the streaming data
    szenario.
'''

# ------------------------------------ streamingDatasetCluster ---------------------------------------

# Imports
import pandas as pd

# get static database connection
from Dashboard import databaseconnection

con = databaseconnection.Connection.db_connection

# ---------------------------- get data from database -----------------------

df = pd.read_sql(
    'SELECT prediction, avgSpeed, avgAbsAcceleration '
    'FROM fleetanalytics.cluster_drivers ', con=con)

cols = ['avgSpeed', 'avgAbsAcceleration', 'prediction']
df = df[cols]
df = df.round({'avgSpeed': 2, 'avgAbsAcceleration': 2})

df[0] = df['avgSpeed'].astype(str)+'\t'+df['avgAbsAcceleration'].astype(str)+'\t'+df['prediction'].astype(str)
df = df.drop(columns=['avgSpeed', 'avgAbsAcceleration', 'prediction'])

# ---------------------------- write csv to output path  ---------------------------------

dftxt = df.to_csv(r'C:\Users\elina\Documents\HdM\Semester6\Data_Science_Project\streamingData.txt', header=None, index=None, sep='\n')

