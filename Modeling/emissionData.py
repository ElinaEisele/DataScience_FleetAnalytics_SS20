'''
    This python contains data science methods of the
    SUMO emission export file.


'''

# --------------------------------------------- emissionData -------------------------------------------

#Imports
import mysql.connector as sql
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import pandasql as ps
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

# Get data from database
from Dashboard import databaseconnection
a = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)
df = pd.read_sql(
    'SELECT * from fleetanalytics.emissions'
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

#Linear Regression
plt.xlabel('speed')
plt.ylabel('CO')
plt.scatter(df.speed,df.CO,color='red',marker='+')
plt.show()

speed=df.speed
print(speed)

CO=df.CO
print(CO)

#Create linear regression object
reg = linear_model.LinearRegression()

#fit = method to train the model using the training set
reg.fit(df[['speed']],df.CO)

#Calculate regression coefficient
a=reg.coef_
print(a)

#Calculate intercept
b=reg.intercept_
print(b)

#Predict CO
print(reg.predict([[11.36]]))

#Control model (y=mx+b), m ist a, b ist b
print(a*0.81+b)

#Predict CO2
print(reg.predict([[0.00]]))

#Control model (y=m+x+b), m ist a, b ist b
print(a*0.00+b)

x=df[['speed']]
y=df[['CO']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept:', model.intercept_)
print('slope:', model.coef_)


#Linear regression
from sklearn import linear_model

plt.xlabel('fuel')
plt.ylabel('COperKM')
plt.scatter(a.fuel,a.COperKM,color='red',marker='+')
plt.show()


# Create linear regression object
reg = linear_model.LinearRegression()

#fit = method to train the model using the training set
reg.fit(a[['fuel']],a.COperKM)

#Calculate regression coefficient
a=reg.coef_
print(a)

#Calculate intercept
b=reg.intercept_
print(b)

#Predict CO
print(reg.predict([[7.7]]))
print(reg.predict([[25]]))

# Read data for line chart
df_line = pd.read_sql(
    'SELECT emissions.fuelKM, emissions.COKM from fleetanalytics.emissions '
    'LIMIT 90000;', con=databaseconnection.Connection.db_connection)

# linear regression to predict CO
x1 = df_line[['fuelKM']]
y1 = df_line[['COKM']]
model = LinearRegression()
model.fit(x1, y1)
plt.xlabel('fuel')
plt.ylabel('CO')
plt.scatter(df_line.fuelKM,df_line.COKM,color='red',marker='+')
plt.show()

x=df[['fuel']]
y=df[['CO']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)

x=df[['fuel']]
y=df[['CO']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)

plt.xlabel('fuel')
plt.ylabel('NOx')
plt.scatter(df.fuel,df.NOx,color='red',marker='+')
plt.show()

x=df[['fuel']]
y=df[['NOx']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)




plt.xlabel('fuel')
plt.ylabel('CO2')
plt.scatter(df.fuel,df.CO2,color='red',marker='+')
plt.show()

x=df[['fuel']]
y=df[['CO2']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)

plt.xlabel('PMx')
plt.ylabel('fuel')
plt.scatter(df.PMx,df.fuel,color='red',marker='+')
plt.show()

x=df[['PMx']]
y=df[['fuel']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)

#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept PMx und CO2:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)


plt.xlabel('fuel')
plt.ylabel('speed')
plt.scatter(df.speed,df.fuel,color='red',marker='+')
plt.show()

x=df[['fuel']]
y=df[['speed']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept PMx und CO2:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)


plt.xlabel('CO')
plt.ylabel('CO2')
plt.scatter(df.CO,df.CO2,color='red',marker='+')
plt.show()

x=df[['CO']]
y=df[['CO2']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept PMx und CO2:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)

plt.xlabel('speed')
plt.ylabel('CO2')
plt.scatter(df.speed,df.CO2,color='red',marker='+')
plt.show()

x=df[['speed']]
y=df[['CO2']]
model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
#the higher the R-squared, the better the model fits your data
print('coefficient of determination:', r_sq)

# a negative value for your constant/intercept should not be a cause for concern. This simply means
# that the expected value on your dependent
# variable will be less than 0 when all independent/predictor variables are set to 0.
print('intercept PMx und CO2:', model.intercept_)

#Calculate regression coefficient
print('slope:', model.coef_)


df['speed'] = df.speed*3.6
print(df.speed)