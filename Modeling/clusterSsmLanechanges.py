'''
    This python file is part of the Data Exploration and Modeling. The lanechange and ssm
    are the basis of a cluster for drivers behavior.
'''

# ---------------------------------------- clusterSsmLanechanges ------------------------------------

# Import
from pyspark import SparkContext, SQLContext
import pyspark.sql.functions as F
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Get get_k_evaluation method from kMeans
from Modeling import kMeans

# set SparkContext
sc = SparkContext()
sql = SQLContext(sc)

# set variabels for database connection
hostname = "database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com"
dbname = "fleetanalytics"
jdbcPort = 3306
username = "admin"
password = "fleetanalytics"

# read data from database
df_lanechanges = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "lanechanges") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load()

df_conf = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "ssm_conflicts") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load()

df_glob = sql.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "ssm_globalmeassures") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load()

# ------------------------------------------ prepare data ---------------------------------------

df_lanechanges = df_lanechanges.select('tripId', 'speed', 'reason', 'origLeaderGap')

# selection of the features for lanechanges
feat_lanechanges_cont = df_lanechanges.select(['tripId', 'speed', 'origLeaderGap']).groupBy('tripId').agg(
    F.expr('percentile_approx(speed, 0.5)').alias('medianSpeed'),
    F.expr('percentile_approx(origLeaderGap, 0.5)').alias('medianOrigLeaderGap')
)
df_lanechanges_cat = df_lanechanges.groupBy('tripId', 'reason').count()
feat_lanechanges_cat = df_lanechanges_cat.groupBy('tripId').pivot('reason').sum('count').na.fill(0)

# selection of the features for conflicts
feat_ssm_conflicts = df_conf.select(['tripId', 'MinTtcTime'])
feat_ssm_conflicts = feat_ssm_conflicts.groupBy('tripId').agg(F.expr('percentile_approx(MinTtcTime, 0.5)').alias('medianMinTtcTime'))

# selection of the features for global measures
feat_ssm_globalmeasures = df_glob.select(['tripId', 'MaxBrValue',
                                                          'MinSgapValue'])
feat_ssm_globalmeasures = feat_ssm_globalmeasures.groupBy('tripId').agg(F.expr('percentile_approx(MaxBrValue, 0.5)').alias('medianMaxBrValue'),
                                                                           F.expr('percentile_approx(MinSgapValue, 0.5)').alias('medianMinSgapValue'))

# joining the feature selections
features_all = feat_ssm_globalmeasures.join(feat_lanechanges_cont, on='tripId', how='inner')

# Outlier detection: tripId: 5071.163
features_all = features_all.filter(features_all['tripId'] != 5071.163)
# features_all.show()
# print(features_all.count())

# cast columns to type double
df_tripId = features_all
cols = ['medianSpeed', 'medianOrigLeaderGap', 'medianMaxBrValue', 'medianMinSgapValue']
features_all = features_all.select([F.col(c).cast("double") for c in cols])


# ========================================= ML =======================================


# -------------------------------------- replace NaN ----------------------------------

from pyspark.ml.feature import Imputer
imputer = Imputer(inputCols=['medianSpeed',
                             'medianOrigLeaderGap',
                             'medianMaxBrValue',
                             'medianMinSgapValue'],
                 outputCols=['medianSpeed',
                             'medianOrigLeaderGap',
                             'medianMaxBrValue',
                             'medianMinSgapValue'])

fitted_imputer = imputer.fit(features_all)
features_all_imputed = fitted_imputer.transform(features_all)


# ------------------------------------ select only features -------------------------------------

feature_columns = ['medianSpeed', 'medianOrigLeaderGap', 'medianMaxBrValue', 'medianMinSgapValue']

# --------------------- Features Transformer / puts multiple columns in one Vector ------------------

from pyspark.ml.feature import VectorAssembler
vecAssembler = VectorAssembler(inputCols=feature_columns,
                               outputCol="features")
df_clustering = vecAssembler.transform(features_all_imputed)

# ---------------------------------------- scale features --------------------------------------------

from pyspark.mllib.util import MLUtils
from pyspark.ml.feature import StandardScaler
scaler = StandardScaler(inputCol="features",
                        outputCol="features_scaled",
                        withStd=True,
                        withMean=False)

# Compute summary statistics by fitting the StandardScaler
scalerModel = scaler.fit(df_clustering)

# Normalize each feature to have unit standard deviation.
scaledData = scalerModel.transform(df_clustering)
scaledData = scaledData.withColumn('medianMinSgapValue', F.round(F.col('medianMinSgapValue'),2))
scaledData = scaledData.withColumn('medianOrigLeaderGap', F.round(F.col('medianOrigLeaderGap'),2))


# ------------------------------------------- get k for k Means ----------------------------------------

#retrieve evaluatioion metrics for different k's
df_evaluation = kMeans.get_k_evaluation(scaledData, 2, 6)

#Plot the silhouette and WSSE for each k that was evaluated. Optimal k has a small WSSE and a bend in the silhouette Coefficient
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x = df_evaluation.index, y = df_evaluation.silhouette, name = 'silhouette'), secondary_y=False,)
fig.add_trace(go.Scatter(x = df_evaluation.index, y = df_evaluation.WSSE, name = 'WSSE (Within Cluster sum of squared error)'), secondary_y = True,)
fig.show()

# ------------------------------------------ train k means model ---------------------------------------------

from pyspark.ml.clustering import KMeans
kmeans = KMeans(k=5,
                seed=100,
                initSteps = 10,
                maxIter=50)
model = kmeans.fit(scaledData.select('features'))

transformed = model.transform(scaledData)
# transformed.show(truncate=False)

# ----------------------------------------  join cluster and tripId -------------------------------------

final_cols = ['tripId', 'medianSpeed','medianOrigLeaderGap', 'medianMaxBrValue', 'medianMinSgapValue', 'prediction']
cluster_tripId_df = transformed.join(df_tripId, on=cols, how='left')
cluster_tripId_df = cluster_tripId_df.select(final_cols)
cluster_tripId_df.show()

# ------------------------------------ principal component analysis (PCA) -------------------------------

t = np.array(transformed.select('prediction').collect())
t = t.tolist()
target = []
for x in t:
    target.append(x[0])
data = np.array(transformed.select('medianSpeed', 'medianOrigLeaderGap', 'medianMaxBrValue', 'medianMinSgapValue').collect())
data = data.tolist()

pca = PCA(n_components=2).fit(data)
pca_2d = pca.transform(data)

print('PCA Dataset :',pca_2d)

#  ----------------------------------------- show cluster as scatter -------------------------------------

import pylab as pl
for i in range(0, pca_2d.shape[0]):
    if target[i] == 0:
        c1 = pl.scatter(pca_2d[i, 0], pca_2d[i, 1], c='r', marker='+')
    elif target[i] == 1:
        c2 = pl.scatter(pca_2d[i, 0], pca_2d[i, 1], c='g', marker='o')
    elif target[i] == 2:
        c3 = pl.scatter(pca_2d[i, 0], pca_2d[i, 1], c='b', marker='*')
    elif target[i] == 3:
        c4 = pl.scatter(pca_2d[i, 0], pca_2d[i, 1], c='black', marker='o')
    elif target[i] == 4:
        c5 = pl.scatter(pca_2d[i, 0], pca_2d[i, 1], c='grey', marker='o')

pl.legend([c1, c2, c3, c4, c5], ['C1', 'C2', 'C3', 'C4', 'C5'])
pl.show()

# ------------------------------------- write cluster dataframe to db -------------------------------------

t = transformed.drop('features', 'features_scaled')
data = t.toPandas().to_dict(orient='list')
dataFrame = pd.DataFrame(data)


tableName = 'ssm_lc_cluster_oAk5'
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