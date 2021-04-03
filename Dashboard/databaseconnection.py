"""
    Contains the database connection object in a class to make it static, which allows for only one
    databaseconnection at a time.
"""

# Beim Packet installieren von mysql.connector nicht das erste auswählen was PyCharm vorschlägt,
# sondern mysql-connector-python
import mysql.connector as sql
import pandas as pd


# Statische Klasse mit der Verbindung zur Datenbank.
class Connection:
    db_connection = sql.connect(host='database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com',
                                database='fleetanalytics', user='admin', password='fleetanalytics')

# Beispiel Abruf, die Tabellen sind sehr groß, deshalb empfehle ich nicht alles abzufragen, sondern ein Limit
# einzubauen.
# df = pd.read_sql('SELECT * from fleetanalytics.lkw_agg2 LIMIT 1000;', con=DBConnection.db_connection)

# print(df)

# Um das ganze zum Beispiel als csv zu speichern.
# df.to_csv("Pfad//hier//angeben")
