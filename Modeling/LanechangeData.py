'''
    This python file contains the first statistics and histograms
    for the export file lanechanges.
'''

# -------------------------------------------- conflict ---------------------------------------

# Imports
import mysql.connector as sql
import pandas as pd
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# ---------------------------------------------- prepare data --------------------------------------

db_connection = sql.connect(host='database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com', database='fleetanalytics', user='admin', password='fleetanalytics')


# Dataframe with SELECT * - Statement
df = pd.read_sql('SELECT * FROM lanechanges', con=db_connection)

#df.columns = ['tripId','time','sec', 'result','from', 'to', 'dir', 'speed', 'reason', 'leaderGab', 'leaderSecureGab', 'leaderSpeed', 'followerGab', 'followerSecureGab', 'followerSpeed', 'OrigLeaderGab', 'origLeaderSecureGab', 'origLeaderSpeed']

print(df.head(100))

print(df.isnull().sum())
print(df.isnull())

print(df.info())
print(df.describe())

# Shows the datatype
print(df.dtypes)

#____Dataframe with reason keepRight____
df2 = pd.read_sql('SELECT * FROM lanechanges WHERE reason ="keepRight"', con=db_connection)
print(df2.head(100))

print(df2.isnull().sum())
print(df2.isnull())

print(df2.info())
print(df2.describe())
print(df2.dtypes)

plt.hist(df2['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()

#plt.hist(df2['reason'])
#plt.xlabel('reason')
#plt.show()

plt.hist(df2['leaderSpeed'])
plt.xlabel('leaderSpeed')
plt.show()

plt.hist(df2['followerSpeed'])
plt.xlabel('followerSpeed')
plt.show()

plt.hist(df2['origLeaderSpeed'])
plt.xlabel('origLeaderSpeed')
plt.show()


# _____________________________SELECT Statement with Python --> takes too long ______________________________
#df4 = pd.read_sql('SELECT * FROM lanechanges LEFT JOIN emissions on lanechanges.tripId = emissions.tripId', con=db_connection)
#print(df4.head(100))


# _____________________________Statement join emissions and lanechanges ____________________________________
df4=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions.csv")

plt.hist(df4['reason'])
plt.xlabel('reason')
plt.ylabel('frequency')
plt.show()


print(df4.head(100))

print(df4.isnull().sum())
print(df4.isnull())

print(df4.info())

#Statistische Metriken anzeigen lassen
print(df4.describe())
#Datentypen anzeigen lassen
print(df4.dtypes)




# ________________________________________Reason keepRight _________________________________________
df5=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions_keepRight.csv")
#print(df5.head(100))
#print(df5.isnull().sum())
#print(df5.isnull())
#print(df5.info())
#print(df5.describe())
#print(df5.dtypes)

df6=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_fcd_keepRight.csv")
print(df6.head(100))
print(df6.isnull().sum())
print(df6.isnull())
print(df6.info())
print(df6.describe())
print(df6.dtypes)

plt.hist(df6['acceleration'])
plt.xlabel('acc')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean absoluteAcc \n", df6.acceleration.mean())
print("\n keepRight Calculate Median absoluteAcc \n", df6.acceleration.median())
print("\n keepRight Calculate Mode absoluteAcc \n", df6.acceleration.mode())


plt.hist(df5['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean SPEED \n", df5.speed.mean())
print("\n keepRight Calculate Median SPEED \n", df5.speed.median())
print("\n keepRight Calculate Mode SPEED \n", df5.speed.mode())

plt.hist(df5['fuel'])
plt.xlabel('fuel')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean FUEL \n", df5.fuel.mean())
print("\n keepRight Calculate Median FUEL \n", df5.fuel.median())
print("\n keepRight Calculate Mode FUEL \n", df5.fuel.mode())

plt.hist(df5['CO2'])
plt.xlabel('CO2')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean CO2 \n", df5.CO2.mean())
print("\n keepRight Calculate Median CO2 \n", df5.CO2.median())
print("\n keepRight Calculate Mode CO2 \n", df5.CO2.mode())

plt.hist(df5['CO'])
plt.xlabel('CO')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean CO \n", df5.CO.mean())
print("\n keepRight Calculate Median CO \n", df5.CO.median())
print("\n keepRight Calculate Mode CO \n", df5.CO.mode())

plt.hist(df5['NOx'])
plt.xlabel('NOx')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean NOx \n", df5.NOx.mean())
print("\n keepRight Calculate Median NOx \n", df5.NOx.median())
print("\n keepRight Calculate Mode NOx \n", df5.NOx.mode())

plt.hist(df5['noise'])
plt.xlabel('noise')
plt.ylabel('frequency')
plt.show()
print("\n keepRight Calculate Mean NOISE \n", df5.noise.mean())
print("\n keepRight Calculate Median NOISE \n", df5.noise.median())
print("\n keepRight Calculate Mode NOISE \n", df5.noise.mode())



# _________________________________________Reason speedGain__________________________________________
df6=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions_speedGain.csv")
print(df6.head(100))
print(df6.isnull().sum())
print(df6.isnull())
print(df6.info())
print(df6.describe())
print(df6.dtypes)

plt.hist(df6['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()
print("\n speedGain Calculate Mean SPEED \n", df6.speed.mean())
print("\n speedGain Calculate Median SPEED \n", df6.speed.median())
print("\n speedGain Calculate Mode SPEED \n", df6.speed.mode())

plt.hist(df6['fuel'])
plt.xlabel('fuel')
plt.ylabel('frequency')
plt.show()
print("\n speedGain Calculate Mean FUEL \n", df6.fuel.mean())
print("\n speedGain Calculate Median FUEL \n", df6.fuel.median())
print("\n speedGain Calculate Mode FUEL \n", df6.fuel.mode())

plt.hist(df6['CO2'])
plt.xlabel('CO2')
plt.ylabel('frequency')
plt.show()
print("\n speedGain Calculate Mean CO2 \n", df6.CO2.mean())
print("\n speedGain Calculate Median CO2 \n", df6.CO2.median())
print("\n speedGain Calculate Mode CO2 \n", df6.CO2.mode())

plt.hist(df6['CO'])
plt.xlabel('CO')
plt.ylabel('frequency')
plt.show()
print("\n speedGain Calculate Mean CO \n", df6.CO.mean())
print("\n speedGain Calculate Median CO \n",df6.CO.median())
print("\n speedGain Calculate Mode CO \n", df6.CO.mode())

plt.hist(df6['NOx'])
plt.xlabel('NOx')
plt.ylabel('frequency')
plt.show()
print("\n speedGain Calculate Mean NOx \n", df6.NOx.mean())
print("\n speedGain Calculate Median NOx \n", df6.NOx.median())
print("\n speedGain Calculate Mode NOx \n", df6.NOx.mode())

plt.hist(df6['noise'])
plt.xlabel('noise')
plt.ylabel('frequency')
plt.show()
print("\n speedGain Calculate Mean NOISE \n", df6.noise.mean())
print("\n speedGain Calculate Median NOISE \n", df6.noise.median())
print("\n speedGain Calculate Mode NOISE \n", df6.noise.mode())



# _________________________________________Reason strategic ________________________________________
df7=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions_strategic.csv")
print(df7.head(100))
print(df7.isnull().sum())
print(df7.isnull())
print(df7.info())
print(df7.describe())
print(df7.dtypes)

plt.hist(df7['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()
print("\n strategic Calculate Mean SPEED \n", df7.speed.mean())
print("\n strategic Calculate Median SPEED \n", df7.speed.median())
print("\n strategic Calculate Mode SPEED \n", df7.speed.mode())


plt.hist(df7['fuel'])
plt.xlabel('fuel')
plt.ylabel('frequency')
plt.show()
print("\n strategic Calculate Mean FUEL \n", df7.fuel.mean())
print("\n strategic Calculate Median FUEL \n", df7.fuel.median())
print("\n strategic Calculate Mode FUEL \n", df7.fuel.mode())

plt.hist(df7['CO2'])
plt.xlabel('CO2')
plt.ylabel('frequency')
plt.show()
print("\n strategic Calculate Mean CO2 \n", df7.CO2.mean())
print("\n strategic Calculate Median CO2 \n", df7.CO2.median())
print("\n strategic Calculate Mode CO2 \n", df7.CO2.mode())

plt.hist(df7['CO'])
plt.xlabel('CO')
plt.ylabel('frequency')
plt.show()
print("\n strategic Calculate Mean CO \n", df7.CO.mean())
print("\n strategic Calculate Median CO \n",df7.CO.median())
print("\n strategic Calculate Mode CO \n", df7.CO.mode())

plt.hist(df7['NOx'])
plt.xlabel('NOx')
plt.ylabel('frequency')
plt.show()
print("\n strategic Calculate Mean NOx \n", df7.NOx.mean())
print("\n strategic Calculate Median NOx \n", df7.NOx.median())
print("\n strategic Calculate Mode NOx \n", df7.NOx.mode())

plt.hist(df7['noise'])
plt.xlabel('noise')
plt.ylabel('frequency')
plt.show()
print("\n strategic Calculate Mean NOISE \n", df7.noise.mean())
print("\n strategic Calculate Median NOISE \n", df7.noise.median())
print("\n strategic Calculate Mode NOISE \n", df7.noise.mode())



#_______________________________________________Reason strategic_urgent______________________________________________
df7=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions_strategic_urgent.csv")
print(df7.head(100))
print(df7.isnull().sum())
print(df7.isnull())
print(df7.info())
print(df7.describe())
print(df7.dtypes)

plt.hist(df7['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()
print("\n strategic_urgent Calculate Mean SPEED \n", df7.speed.mean())
print("\n strategic_urgent Calculate Median SPEED \n", df7.speed.median())
print("\n strategic_urgent Calculate Mode SPEED \n", df7.speed.mode())


plt.hist(df7['fuel'])
plt.xlabel('fuel')
plt.ylabel('frequency')
plt.show()
print("\n strategic_urgent Calculate Mean FUEL \n", df7.fuel.mean())
print("\n strategic_urgent Calculate Median FUEL \n", df7.fuel.median())
print("\n strategic_urgent Calculate Mode FUEL \n", df7.fuel.mode())

plt.hist(df7['CO2'])
plt.xlabel('CO2')
plt.ylabel('frequency')
plt.show()
print("\n strategic_urgent Calculate Mean CO2 \n", df7.CO2.mean())
print("\n strategic_urgent Calculate Median CO2 \n", df7.CO2.median())
print("\n strategic_urgent Calculate Mode CO2 \n", df7.CO2.mode())

plt.hist(df7['CO'])
plt.xlabel('CO')
plt.ylabel('frequency')
plt.show()
print("\n strategic_urgent Calculate Mean CO \n", df7.CO.mean())
print("\n strategic_urgent Calculate Median CO \n",df7.CO.median())
print("\n strategic_urgent Calculate Mode CO \n", df7.CO.mode())

plt.hist(df7['NOx'])
plt.xlabel('NOx')
plt.ylabel('frequency')
plt.show()
print("\n strategic_urgent Calculate Mean NOx \n", df7.NOx.mean())
print("\n strategic_urgent Calculate Median NOx \n", df7.NOx.median())
print("\n strategic_urgent Calculate Mode NOx \n", df7.NOx.mode())

plt.hist(df7['noise'])
plt.xlabel('noise')
plt.ylabel('frequency')
plt.show()
print("\n strategic_urgent Calculate Mean NOISE \n", df7.noise.mean())
print("\n strategic_urgent Calculate Median NOISE \n", df7.noise.median())
print("\n strategic_urgent Calculate Mode NOISE \n", df7.noise.mode())


# ________________________________________________Reason cooperative_____________________________________
df7=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions_cooperative.csv")
print(df7.head(100))
print(df7.isnull().sum())
print(df7.isnull())
print(df7.info())
print(df7.describe())
print(df7.dtypes)

plt.hist(df7['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()
print("\n cooperative Calculate Mean SPEED \n", df7.speed.mean())
print("\n cooperative Calculate Median SPEED \n", df7.speed.median())
print("\n cooperative Calculate Mode SPEED \n", df7.speed.mode())

plt.hist(df7['fuel'])
plt.xlabel('fuel')
plt.ylabel('frequency')
plt.show()
print("\n cooperative Calculate Mean FUEL \n", df7.fuel.mean())
print("\n cooperative Calculate Median FUEL \n", df7.fuel.median())
print("\n cooperative Calculate Mode FUEL \n", df7.fuel.mode())

plt.hist(df7['CO2'])
plt.xlabel('CO2')
plt.ylabel('frequency')
plt.show()
print("\n cooperative Calculate Mean CO2 \n", df7.CO2.mean())
print("\n cooperative Calculate Median CO2 \n", df7.CO2.median())
print("\n cooperative Calculate Mode CO2 \n", df7.CO2.mode())

plt.hist(df7['CO'])
plt.xlabel('CO')
plt.ylabel('frequency')
plt.show()
print("\n cooperative Calculate Mean CO \n", df7.CO.mean())
print("\n cooperative Calculate Median CO \n",df7.CO.median())
print("\n cooperative Calculate Mode CO \n", df7.CO.mode())

plt.hist(df7['NOx'])
plt.xlabel('NOx')
plt.ylabel('frequency')
plt.show()
print("\n cooperative Calculate Mean NOx \n", df7.NOx.mean())
print("\n cooperative Calculate Median NOx \n", df7.NOx.median())
print("\n cooperative Calculate Mode NOx \n", df7.NOx.mode())

plt.hist(df7['noise'])
plt.xlabel('noise')
plt.ylabel('frequency')
plt.show()
print("\n cooperative Calculate Mean NOISE \n", df7.noise.mean())
print("\n cooperative Calculate Median NOISE \n", df7.noise.median())
print("\n cooperative Calculate Mode NOISE \n", df7.noise.mode())



#___________________________________________Reason ooperative_urgent __________________________________
df7=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_emissions_cooperative_urgent.csv")
print(df7.head(100))
print(df7.isnull().sum())
print(df7.isnull())
print(df7.info())
print(df7.describe())
print(df7.dtypes)

plt.hist(df7['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()
print("\n cooperative_urgent Calculate Mean SPEED \n", df7.speed.mean())
print("\n cooperative_urgent Calculate Median SPEED \n", df7.speed.median())
print("\n cooperative_urgent Calculate Mode SPEED \n", df7.speed.mode())

plt.hist(df7['fuel'])
plt.xlabel('fuel')
plt.ylabel('frequency')
plt.show()
print("\n cooperative_urgent Calculate Mean FUEL \n", df7.fuel.mean())
print("\n cooperative_urgent Calculate Median FUEL \n", df7.fuel.median())
print("\n cooperative_urgent Calculate Mode FUEL \n", df7.fuel.mode())

plt.hist(df7['CO2'])
plt.xlabel('CO2')
plt.ylabel('frequency')
plt.show()
print("\n cooperative_urgent Calculate Mean CO2 \n", df7.CO2.mean())
print("\n cooperative_urgent Calculate Median CO2 \n", df7.CO2.median())
print("\n cooperative_urgent Calculate Mode CO2 \n", df7.CO2.mode())

plt.hist(df7['CO'])
plt.xlabel('CO')
plt.ylabel('frequency')
plt.show()
print("\n cooperative_urgent Calculate Mean CO \n", df7.CO.mean())
print("\n cooperative_urgent Calculate Median CO \n",df7.CO.median())
print("\n cooperative_urgent Calculate Mode CO \n", df7.CO.mode())

plt.hist(df7['NOx'])
plt.xlabel('NOx')
plt.ylabel('frequency')
plt.show()
print("\n cooperative_urgent Calculate Mean NOx \n", df7.NOx.mean())
print("\n cooperative_urgent Calculate Median NOx \n", df7.NOx.median())
print("\n cooperative_urgent Calculate Mode NOx \n", df7.NOx.mode())

plt.hist(df7['noise'])
plt.xlabel('noise')
plt.ylabel('frequency')
plt.show()
print("\n cooperative_urgent Calculate Mean NOISE \n", df7.noise.mean())
print("\n cooperative_urgent Calculate Median NOISE \n", df7.noise.median())
print("\n cooperative_urgent Calculate Mode NOISE \n", df7.noise.mode())


# ------------------ Absolute Acceleration with mean, median and mode of the different lanechange reasons --------------

df6=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/lkw_join_lanechanges_fcd_cooperative.csv")
plt.hist(df6['absoluteAcc'])
plt.xlabel('absoluteAcc')
plt.ylabel('frequency')
plt.show()
print("\n  Calculate Mean absoluteAcc \n", df6.absoluteAcc.mean())
print("\n  Calculate Median absoluteAcc \n", df6.absoluteAcc.median())
print("\n  Calculate Mode absoluteAcc \n", df6.absoluteAcc.mode())


df7=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/join_lanechanges-fcd/lkw_join_lanechanges_fcd_cooperative_+.csv")
plt.hist(df7['acceleration'])
plt.xlabel('+ acceleration')
plt.ylabel('frequency')
plt.show()
print("\n  Calculate Mean + acc \n", df7.acceleration.mean())
print("\n  Calculate Median + acc \n", df7.acceleration.median())
print("\n  Calculate Mode + acc \n", df7.acceleration.mode())

df8=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/aktuell/join_lanechanges-fcd/lkw_join_lanechanges_fcd_cooperative_-.csv")
plt.hist(df8['acceleration'])
plt.xlabel('- acceleration')
plt.ylabel('frequency')
plt.show()
print("\n  Calculate Mean - acc \n", df8.acceleration.mean())
print("\n  Calculate Median - acc \n", df8.acceleration.median())
print("\n  Calculate Mode - acc \n", df8.acceleration.mode())