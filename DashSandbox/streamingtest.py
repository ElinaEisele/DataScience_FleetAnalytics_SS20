"""
    First attempt at setting up the streaming scenario, here using parallel processes. In the final version
    of the dashboard, this was done using a timed event provided by the Dash-Framework
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import plotly.express as px
from multiprocessing import Process
from DashSandbox import sensor

# Hier ist die statische Klasse mit der Verbindung zur Datenbank. Durch die statische Eigenschaft wird sichergestellt,
# das pro Instanz dieser App nur eine Verbindung zur Datenbank aufgebaut wird.
from Dashboard import databaseconnection

avgCO2 = 1


def visualize():
    # Get training data set
    df = pd.read_sql('SELECT * from fleetanalytics.agg LIMIT 1000;', con=databaseconnection.Connection.db_connection)

    # Remove rows with NaN values
    df = df.dropna()

    # Train cluster model
    kmeans = KMeans(n_clusters=3)
    labels = kmeans.fit_predict(df[['duration', 'avgCO2']])

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

        html.H6(id='output', children='Enter values'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,
            n_intervals=0
        )

    ])

    @app.callback(dash.dependencies.Output('output', 'children'),
                  [dash.dependencies.Input('interval-component', 'n_intervals')])
    def auto_update(n):
        global avgCO2
        time = 79269 + (n * 10)
        duration = time - 79269

        currentData = sensor.main(time)
        # duration = time - 79269
        avgCO2 += currentData.iloc[0]['CO2']
        co2 = avgCO2/n

        toPredict = [[float(duration), float(co2)]]

        cluster = kmeans.predict(toPredict)
        print(cluster)
        return "Timestep {} {}".format(n, str(np.around(cluster[0])))

    app.run_server(debug=True, use_reloader=False)


if __name__ == '__main__':
    # Main Process with the Dash App
    p1 = Process(target=visualize)
    p1.start()

    # Second Process which simulates a driving truck
    # p2 = Process(target=sensor.main())
    # p2.start()
