"""
    Contains the blue boxes with metadata across the entire fleet, used in all panels.
"""

import dash_html_components as html
import pandas as pd

from Dashboard import databaseconnection

# Query database to get the average fuel consumption of the fleet
dfAvergeFuel = pd.read_sql("SELECT avg((avgFuel)/(routeLength/10000)) FROM fleetanalytics.agg;",
                           con=databaseconnection.Connection.db_connection)
fleetAverageFuel = round(float(dfAvergeFuel.values[0]), 2)
fleetAverageFuelTitle = "Ø Dieselverbrauch"
fleetAverageFuelUnit = "Liter/km"

# Query database for number of drivers
dfCountDrivers = pd.read_sql("SELECT count(distinct(driverId)) FROM agg_on_drivers;",
                             con=databaseconnection.Connection.db_connection)
driverCount = int(dfCountDrivers.values[0])
driverCountTitle = "Anzahl Fahrer"
driverCountUnit = "Fahrer"

# Query the database for the total distance driven by the fleet
dfTotalDistance = pd.read_sql("select sum(routeLength) from trip;",
                              con=databaseconnection.Connection.db_connection)
totalDistance = round(float(dfTotalDistance.values[0]), 2)

averageDrivingDistance = round(float(totalDistance/driverCount), 2)

flexBox = html.Div(
    className="parentBox",
    children=[
        html.Div(
            className="metadatabox",
            children=[
                html.Span("Anzahl Fahrer", className="andereZahl"),
                html.Br(),
                html.Div(
                    className="kennZahlIcon",
                    children=[
                        html.Img(src="https://image.flaticon.com/icons/svg/1532/1532082.svg", className="fahrerIcon"),
                        html.Span(driverCount, className="kennZahl")
                    ]
                ),
                html.Span("Fahrer", className="andereZahl")
            ]
        ),
        html.Div(
            className="metadatabox",
            children=[
                html.Span("Ø Dieselverbrauch", className="andereZahl"),
                html.Br(),
                html.Span(fleetAverageFuel, className="spritZahl kennZahl"),
                html.Br(),
                html.Span("Liter/km", className="andereZahl")
            ]
        ),
        html.Div(
            className="metadatabox",
            children=[
                html.Span("Ø Strecke pro Fahrer", className="andereZahl"),
                html.Br(),
                html.Span(averageDrivingDistance, className="kennZahl"),
                html.Br(),
                html.Span("km", className="andereZahl")
            ]
        ),
    ]
)
