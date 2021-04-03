"""
    These methods are used to convert the raw data from the Bundesamt für Straßenwesen for them to be used
    with the SUMO simulation.
    Input: Bast Data, hourly
    Output: flow.csv for SUMO DFROUTER
"""

import pandas as pd
from datetime import datetime

# Remove whitespaces
# with open(r'C:\\Users\\wahl_\\Downloads\\2018_B_S\\2018_B_S.txt', 'r') as infile, \
#      open(r'C:\\Users\\wahl_\\Downloads\\2018_B_S\\NoWhitespaces_2018_B_S.txt', 'w') as outfile:
#     data = infile.read()
#     data = data.replace(" ", "")
#     outfile.write(data)

# Extract just Berlin for testing purposes.
# for chunk in pd.read_csv("C:\\Users\\wahl_\\Downloads\\2018_A_S\\2018_A_S.txt", chunksize=100000, delimiter=";"):
#     df = chunk.loc[chunk['Land'] == 11]
#     if not df.empty:
#         print("Berlin Autobahn Data found")
#         df.to_csv("C:\\Users\\wahl_\\Downloads\\2018_A_S\\berlin_only.csv", mode='a')

# Adding Bundesstraßen
# for chunkB in pd.read_csv("C:\\Users\\wahl_\\Downloads\\2018_B_S\\NoWhitespaces_2018_B_S.txt", chunksize=100000,
#                           delimiter=";"):
#     dfb = chunkB.loc[chunkB['Land'] == 11]
#     if not dfb.empty:
#         print('Berlin Bundestraße found')
#         dfb.to_csv("C:\\Users\\wahl_\\Downloads\\2018_A_S\\berlin_only.csv", mode='a', header=False)

# Combine Autobahn and Bundesstraßen for all of Germany
# x = 0
# for chunk in pd.read_csv("E:\\FleetAnalytics\\Input\\2018_A_S\\2018_A_S.txt", chunksize=100000, delimiter=";"):
#     if x == 0:
#         chunk.to_csv("E:\\FleetAnalytics\\Input\\PreparedData\\stundendaten_deutschland_komplett.csv", mode="a")
#         x = x+1
#     else:
#         chunk.to_csv("E:\\FleetAnalytics\\Input\\PreparedData\\stundendaten_deutschland_komplett.csv", mode="a",
#                  header=False)
#
# for chunk in pd.read_csv("E:\\FleetAnalytics\\Input\\2018_B_S\\NoWhitespaces_2018_B_S.txt", chunksize=100000,
#                          delimiter=";"):
#     chunk.to_csv("E:\\FleetAnalytics\\Input\\PreparedData\\stundendaten_deutschland_komplett.csv", mode="a",
#                  header=False)

x = 0
# Read Berlin file
for df in pd.read_csv('E:\\FleetAnalytics\\Input\\PreparedData\\stundendaten_deutschland_komplett.csv',
                      chunksize=100000):
    # Calculate, how many days have passed since 01.01.2018
    def dostuff(datetoprocess):
        e_date = datetime.strptime('180101', '%y%m%d')
        delta = datetoprocess - e_date
        return delta


    # Convert Date to String
    df['Datum'] = df['Datum'].astype(str)
    # -1 to get acutal hours from index
    df['Stunde'] = df['Stunde'] - 1
    df['Stunde'] = df['Stunde'].astype(str)
    # Convert to pandas datetime format
    df['time'] = pd.to_datetime(df['Datum'] + " " + df['Stunde'], format='%y%m%d %H', errors='coerce')
    # Calculate how many days since start of year
    df['time'] = dostuff(df['time'])
    # Convert to minutes and save as int
    df['time'] = pd.to_timedelta(df['time']).astype('timedelta64[m]').astype(int)
    # Add columns with the average speed
    df['vPKW'] = 100
    df['vLKW'] = 80

    # Cleanup and saving
    df.rename(columns={'Zst': 'Detector', 'time': 'Time', 'KFZ_R1': 'qPKW', 'Lkw_R1': 'qLKW'}, inplace=True)
    dfout = df[['Detector', 'Time', 'qPKW', 'qLKW', 'vPKW', 'vLKW']]
    print(dfout)
    if x == 0:
        dfout.to_csv('E:\\FleetAnalytics\\Input\\PreparedData\\deutschland_final.csv', sep=";", index=False, mode='a')
        x = x+1
    else:
        dfout.to_csv('E:\\FleetAnalytics\\Input\\PreparedData\\deutschland_final.csv', sep=";", index=False, mode='a', header=False)

