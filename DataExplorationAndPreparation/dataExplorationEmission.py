'''
    This python file develops shows the data exploration of the
    SUMO emission export file.


'''

# ---------------------------- dataExplorationEmission -----------------------

#Imports
import pandas as pd
from matplotlib import pyplot as plt
import pandas as pd

# Get data from database
from Dashboard import databaseconnection

#Read data
df=pd.read_csv("/Users/emily/Desktop/Daten DS/emission data.csv")

#Show the first hundred data
print(df.head(100))

#Show missing values (nan, NaN, "") per column
print(df.isnull().sum())
print(df.isnull())

print(df.info())

#describe typically metrics
print(df.describe())

#Control datatypes
print(df.dtypes)

#Show data where HC is 0
print(df[(df.HC == 0)])
df.to_excel("/Users/emily/Desktop/Zwischenergebnisse.xlsx")

#Show data where fuel values are 0 to control the fact that emission values are zero while braking
a=df[(df.fuel == 0)]
print(a)
a.to_excel("/Users/emily/Desktop/Zwischenergebnisse.xlsx")

#Show histograms
plt.hist(df['CO'])
plt.xlabel('CO')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['CO2'])
plt.xlabel('CO2')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['NOx'])
plt.xlabel('NOx')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['PMx'])
plt.xlabel('PMx')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['fuel'])
plt.xlabel('fuel')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['noise'])
plt.xlabel('noise')
plt.ylabel('Frequency')
plt.show()

plt.hist(df['speed'])
plt.xlabel('speed')
plt.ylabel('Frequency')
plt.show()

#Show boxplots to detect outliers
plt.boxplot(df["CO"])
plt.show()

plt.boxplot(df["CO2"])
plt.show()
plt.boxplot(df["speed"])
plt.show()

#Read data
df2 = pd.read_sql(
    'SELECT emissions.NOxGrenzwerte from fleetanalytics.emissions '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

#Show histogram
plt.hist(df2['NOxGrenzwerte'], bins=20)
plt.xlabel('NOxGrenzwerte')
plt.ylabel('Frequency')
plt.show()