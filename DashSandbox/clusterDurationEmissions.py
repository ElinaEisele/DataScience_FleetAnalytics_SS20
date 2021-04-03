'''
    First prototype for a kmeans cluster with visualization in a scatter plot. This later became the part of the
    "Plan a Trip" panel in the final dashboard.
'''

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px

# Hier ist die statische Klasse mit der Verbindung zur Datenbank. Durch die statische Eigenschaft wird sichergestellt,
# das pro Instanz dieser App nur eine Verbindung zur Datenbank aufgebaut wird.
from Dashboard import databaseconnection

# Get training data set
df = pd.read_sql('SELECT * from fleetanalytics.agg LIMIT 1000;', con=databaseconnection.Connection.db_connection)

# Remove rows with NaN values
df = df.dropna()

# Train cluster model
kmeans = KMeans(n_clusters=3)
labels = kmeans.fit_predict(df)

# Transform result into dataframe and add column 'label' onto training data set
labelsdf = pd.DataFrame(labels, columns=['label'])
result = pd.concat([df, labelsdf], axis=1, sort=False)

# Convert the label column to string
result.label = result.label.astype(str)

# Build graph
fig = px.scatter(result, y="duration", x="avgCO2", color="label")

# Layout des Scatterplot anpassen
fig.update_layout(
    title="K-Means Cluster",
    xaxis_title="duration",
    yaxis_title="avgCO2",
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Daten aus AWS Datenbank'),
    dcc.Graph(figure=fig),

])

if __name__ == '__main__':
    app.run_server(debug=True)
