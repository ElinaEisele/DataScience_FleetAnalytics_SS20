'''
    This python file is part of the Data Preperation and creates fake driverIds.
'''

# -------------------------------------- dataPreperationDriverProfiles --------------------------

# Imports
import pandas as pd
import numpy as np
import random

# Get static database connection object
from Dashboard import databaseconnection

con = databaseconnection.Connection.db_connection

# ---------------------------- get data from database -----------------------

cluster_df = pd.read_sql(
    'SELECT tripId, prediction FROM fleetanalytics.cluster_Fahrerprofile_tripId_k3 cf '
    'ORDER BY cf.prediction',
    con=con)

#  -------------------------- create driver id --------------------------------------------

cluster_df['driverId'] = np.nan
cluster_df_0 = cluster_df[cluster_df['prediction'] == 0]
cluster_df_1 = cluster_df[cluster_df['prediction'] == 1]
cluster_df_2 = cluster_df[cluster_df['prediction'] == 2]

dfs = [cluster_df_0, cluster_df_1, cluster_df_2]


driver = 'driver_'
id=0
d = 0
drCount = random.randint(25,33)

row=-1

for df in dfs:
    start = row + 1
    end = start + len(df)
    id+=1

    for row in range(start, end):
        if d < drCount:
            df['driverId'].loc[row] = driver + str(id)
            d += 1
        else:
            drCount = random.randint(25, 33)
            d = 0
            id += 1
            df['driverId'].loc[row] = driver + str(id)


df = cluster_df_0.append(cluster_df_1)
df = df.append(cluster_df_2)

df_driver = df.drop(['prediction'], axis=1)
print(df_driver)


# ------------------ write to database with pyspark ----------------------------

hostname = "database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com"
dbname = "fleetanalytics"
jdbcPort = 3306
username = "admin"
password = "fleetanalytics"

# tableName = 'trip_driver_id'
# sqlEngine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(username, password, hostname, dbname), pool_recycle=jdbcPort)
# dbConnection = sqlEngine.connect()
#
# try:
#     df_driver.to_sql(tableName, con=dbConnection, if_exists='append')
#
# except ValueError as vx:
#     print('ValueError',vx)
#
# except Exception as ex:
#     print('Exception',ex)
#
# else:
#     print("Table %s created successfully."%tableName)
#
# finally:
#     dbConnection.close()

