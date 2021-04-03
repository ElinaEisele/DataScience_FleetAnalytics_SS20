'''
    This python file shows the Data Exploration of the export file lanechanges
'''

# -------------------------------------------- dataExplorationLanechange ---------------------------------------

# Imports
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# ---------------------------------------------- prepare data --------------------------------------

# First testing with csv file
df=pd.read_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/lkw_lanechange_neu.csv")

#df.columns = ['vehicleId','type','time', 'from','to', 'direction', 'speed', 'position', 'reason', 'leaderGab', 'leaderSecureGab', 'leaderSpeed', 'followerGab', 'followerSecureGab', 'followerSpeed', 'OrigLeaderGab', 'origLeaderSecureGab', 'origLeaderSpeed']
df.columns = ['tripId','time','sec', 'result','from', 'to', 'dir', 'speed', 'reason', 'leaderGab', 'leaderSecureGab', 'leaderSpeed', 'followerGab', 'followerSecureGab', 'followerSpeed', 'OrigLeaderGab', 'origLeaderSecureGab', 'origLeaderSpeed']

# Shows the first 100 rows
print(df.head(100))


# Cleaning (0 -> 'None')
#df.replace(0, 'None', inplace=True)
#df['leaderGab'] = df['leaderGab'].str.replace('0','None')
#df.leaderGab[df.leaderGab == 0] = pd.np.nan
#df.leaderSecureGab[df.leaderSecureGab == 0] = pd.np.nan
#df.leaderSpeed[df.leaderSpeed == 0] = pd.np.nan
#df.followerGab[df.followerGab == 0] = pd.np.nan
#df.replace(None, np.nan)
#df.replace(to_replace='None', value= np.nan)


# Convert m/s to km/h in column with speed
#df['speed'] = df.speed*3.6
#df['leaderSpeed'] = df.leaderSpeed*3.6
#df['followerSpeed'] = df.followerSpeed*3.6
#df['origLeaderSpeed'] = df.origLeaderSpeed*3.6

print(df.isnull().sum())
print(df.isnull())
print(df.info())
print(df.describe())

# Show the data types
print(df.dtypes)

# Exports
df.to_excel("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/Zwischenergebnis_excel.xlsx")
df.to_csv("C:/Users/inesw/Documents/HdM_Desktop/7.Semester/Data Science Projekt/Daten/Zwischenergebnis_csv.csv")

plt.hist(df['leaderGab'])
plt.xlabel('leaderGab')
plt.ylabel('frequency')
plt.show()

plt.hist(df['followerGab'])
plt.xlabel('followerGab')
plt.ylabel('frequency')
plt.show()

#plt.hist(df['origLeaderGab'])
#plt.xlabel('origLeaderGab')
#plt.ylabel('frequency')
#plt.show()

plt.hist(df['speed'])
plt.xlabel('speed')
plt.ylabel('frequency')
plt.show()

#plt.hist(df['position'])
#plt.xlabel('position')
#plt.ylabel('frequency')
#plt.show()


plt.hist(df['reason'])
plt.xlabel('reason')
plt.ylabel('frequency')
plt.show()


plt.boxplot(df['speed'])
plt.show()

#plt.boxplot(df['position'])
#plt.show()

# _______________________________ linearRegression ________________________________________

from sklearn.linear_model import LinearRegression

#x=df[['speed']]
#y=df[['position']]
#model = LinearRegression()
#model.fit(x, y)

#r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
#print('coefficient of determination:', r_sq)
# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
#print('intercept:', model.intercept_)
#print('slope:', model.coef_)

#plt.scatter(df.speed,df.position,color='red',marker='*')
#plt.show()


x=df[['tripId']]
y=df[['speed']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
# the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)
# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept:', model.intercept_)
print('slope:', model.coef_)

plt.scatter(df.tripId,df.speed,color='red',marker='*')
plt.show()

