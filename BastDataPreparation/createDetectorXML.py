'''
    Maps the coordinates of traffic detectors to a map and saves the mapping in an XML-Format
'''

import sumolib
import pyproj
import pandas as pd
import numpy as np

path = 'E:\\FleetAnalytics\\Input\\Detectors\\'
coordinates_file = path + 'stationenKoords.csv'
detector_file = 'detectors2.xml'
net_file = path + 'germany_Autobahn_Bundesstrassen_only.net.xml'

# csv to array
df_coordinates = pd.read_csv(coordinates_file, float_precision='round_trip', nrows=2)
#df_coordinates = df_coordinates.rename(columns = {' longitude':'longitude',' latitude':'latitude'})
df_id_lan_lat = df_coordinates[['DZ_Nr', 'longitude', 'latitude']]
array_coordinates = df_id_lan_lat.to_numpy()
array_coordinates_list = array_coordinates.tolist()

# convert detecor id from float to int
for row in range(0,len(array_coordinates_list)):
    array_coordinates_list[row][0] = int(array_coordinates_list[row][0])

print("Reading net.xml file...")
net = sumolib.net.readNet(net_file)
print("Reading xml file done.")

index = 0
length = len(array_coordinates_list)

detectors = []
for id, lon, lat in array_coordinates_list:
    print(str(index) + " out of " + str(length))
    index = index + 1
    #print(id, lon, lat)
    xy_pos = net.convertLonLat2XY(lon, lat)
    # look 10m around the position
    lanes = net.getNeighboringLanes(xy_pos[0], xy_pos[1], 10)
    # attention, result is unsorted
    bestLane = None
    ref_d = 9999.
    for lane, dist in lanes:
            if dist < ref_d:
                ref_d = dist
                bestLane = lane
                #print('Best lane ', bestLane.getID)
            pos, d = bestLane.getClosestLanePosAndDist(xy_pos)
    try:
        detectors.append(sumolib.sensors.inductive_loop.InductiveLoop(id, bestLane.getID(), pos))
    except:
        print("Error occured " + str(id))

print(detectors)
sumolib.files.additional.write(detector_file, detectors)

