'''
  This python file contains the kMeans method wchich is used in the file
  createClusterDrivingProfiles.py.
'''

# --------------------------------------------- kMeans -------------------------------------------

# Import
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd

# ---------------------------------------------- get k for K Means -----------------------------------------

# Evaluation for number of Clusters
# Calculates the best value for k
# @Input df_prepared: prepared Dataframe
# @Input min_k: minimum value for k
# @Input min_k: minimum value for k

def get_k_evaluation(df_prepared, min_k, max_k):
  df_evaluation = pd.DataFrame(columns = ['silhouette', 'WSSE'])
  for k in range(min_k, max_k):
    kmeans = KMeans(seed=100,
                    initSteps = 10,
                    maxIter=50).setFeaturesCol('features_scaled').setK(k)
    model = kmeans.fit(df_prepared)
    # Make predictions
    predictions = model.transform(df_prepared)

    # Evaluate clustering by computing Silhouette score
    evaluator = ClusteringEvaluator()
    silhouette = evaluator.evaluate(predictions)
    cost = model.computeCost(df_prepared)
    df_evaluation.loc[k,:]= [silhouette,cost]
  return df_evaluation

#Plot evaluation for each k. This can be used to determine the optimal k for the data
#@Input df_evaluation: dataframe containing the Silhouette and Within-Cluster Sum of Squared Error
def plot_evaluation(df_evaluation):
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  # Add traces
  fig.add_trace(go.Scatter(x = df_evaluation.index, y = df_evaluation.silhouette, name = 'silhouette'), secondary_y=False,)
  fig.add_trace(go.Scatter(x = df_evaluation.index, y = df_evaluation.WSSE, name = 'WSSE'), secondary_y = True,)
  return fig