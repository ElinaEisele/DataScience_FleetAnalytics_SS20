'''
    This python file creates a cluster for driving profiles by getting k for
    k-means and apply the model for k clusters.
'''

# ---------------------------------------- createClusterDrivingProfiles -----------------------------------

# Import
import pyspark.sql.functions as F
from pyspark import SparkContext, SQLContext
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd

# get kMeans method from other python file
from Modeling import kMeans

# set SparkContext
sc = SparkContext()
sql = SQLContext(sc)


# ----------------------------------- get data from database -----------------------------------

hostname = "database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com"
dbname = "fleetanalytics"
jdbcPort = 3306
username = "admin"
password = "fleetanalytics"

df_agg = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "agg_on_drivers") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load()

df_agg = df_agg.select('driverId','totalLanechanges', 'avgLanechangeSpeed', 'avgCO2', 'avgSpeed', 'avgAbsAcceleration')
df_agg_tripId = df_agg

cols = ['totalLanechanges', 'avgLanechangeSpeed', 'avgCO2', 'avgSpeed', 'avgAbsAcceleration']
df_agg = df_agg.select([F.col(c).cast("double") for c in cols])


# ============================================ ML =================================================


# --------------------------------------- replace NaN ----------------------------------------------

from pyspark.ml.feature import Imputer
imputer = Imputer(inputCols=['totalLanechanges', 'avgLanechangeSpeed', 'avgCO2', 'avgSpeed', 'avgAbsAcceleration'],
                 outputCols=['totalLanechanges', 'avgLanechangeSpeed', 'avgCO2', 'avgSpeed', 'avgAbsAcceleration'])

fitted_imputer = imputer.fit(df_agg)
features_all_imputed = fitted_imputer.transform(df_agg)


# -------------------- Features Transformer / puts multiple columns in one Vector ----------------------

from pyspark.ml.feature import VectorAssembler
vecAssembler = VectorAssembler(inputCols=cols,
                               outputCol="features")
df_clustering = vecAssembler.transform(features_all_imputed)


# ------------------------------------------- scale features --------------------------------------------

from pyspark.ml.feature import StandardScaler
scaler = StandardScaler(inputCol="features",
                        outputCol="features_scaled",
                        withStd=True,
                        withMean=False)

# Compute summary statistics by fitting the StandardScaler
scalerModel = scaler.fit(df_clustering)

# Normalize each feature to have unit standard deviation.
scaledData = scalerModel.transform(df_clustering)


# ------------------------------------ Methoden anwenden auf Cluster Anzahl ----------------------------

# retrieve evaluatioion metrics for different k's
df_evaluation = kMeans.get_k_evaluation(scaledData, 2, 7)

#Plot the silhouette and WSSE for each k that was evaluated. Optimal k has a small WSSE and a bend in the silhouette Coefficient
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x = df_evaluation.index, y = df_evaluation.silhouette, name = 'silhouette'), secondary_y=False,)
fig.add_trace(go.Scatter(x = df_evaluation.index, y = df_evaluation.WSSE, name = 'WSSE (Within Cluster sum of squared error)'), secondary_y = True,)
fig.show()


# --------------------------------------------- train k means model ------------------------------------------

from pyspark.ml.clustering import KMeans
kmeans = KMeans(k=3,
                seed=100,
                initSteps = 10,
                maxIter=50)
model = kmeans.fit(scaledData.select('features'))

transformed = model.transform(scaledData)
transformed.show(truncate=False)


# -------------------------------------  join cluster and tripId ---------------------------------------

final_cols = ['driverId', 'totalLanechanges', 'avgLanechangeSpeed', 'avgCO2', 'avgSpeed', 'avgAbsAcceleration', 'prediction']
cluster_tripId_df = transformed.join(df_agg_tripId, on=cols, how='left')
cluster_tripId_df = cluster_tripId_df.select(final_cols)
# cluster_tripId_df.show()


# ------------------------------------------ write to database -----------------------------------

from sqlalchemy import create_engine

data = cluster_tripId_df.toPandas().to_dict(orient='list')
dataFrame = pd.DataFrame(data)

tableName = 'cluster_drivers'
sqlEngine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(username, password, hostname, dbname), pool_recycle=jdbcPort)
dbConnection = sqlEngine.connect()

try:
    dataFrame.to_sql(tableName, con=dbConnection, if_exists='append')

except ValueError as vx:
    print('ValueError',vx)

except Exception as ex:
    print('Exception',ex)

else:
    print("Table %s created successfully."%tableName)

finally:
    dbConnection.close()

