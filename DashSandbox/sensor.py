"""
    Used to test database connection to supply simulated driving data
"""

from Dashboard import databaseconnection
import pandas as pd


def main(time):
    driving = pd.read_sql(
        "SELECT * from fleetanalytics.emissions where tripId='1607.16950' AND time='{}'".format(str(time)),
        con=databaseconnection.Connection.db_connection)
    return driving
