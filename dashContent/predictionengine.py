"""
    Sets up a connection to our PredictionIO server and gets driving data for the simulation
"""


import base64
import predictionio
import pandas as pd
from Dashboard import databaseconnection

#394.17150
#5071.42800
df_simu_fcd = pd.read_sql("SELECT * from fleetanalytics.fcd WHERE tripId='394.17150' LIMIT 100;",
                          con=databaseconnection.Connection.db_connection)
length = len(df_simu_fcd.index)

# Mockup image encode
cluster0 = './assets/cluster0.png'
cluster1 = './assets/cluster1.png'
cluster2 = './assets/cluster2.png'


def encode_image(filename):
    return base64.b64encode(open(filename, 'rb').read())


# Connect to PredictionIO
engine_client = predictionio.EngineClient(url="http://35.224.110.205:8000")

# -----------------------------------------Example of asynchronous PredictionIO Engine query----------------------------
# # Create the request and send it asynchronously.
# request = engine_client.asend_query({"dataPoint": [113.98, 0.33]})
#
# # When the result returns, do something.
# try:
#     result = request.get_response()
#     print(result)
# except:
#     print("Something went wrong with the response from the PredictionIO server.")
