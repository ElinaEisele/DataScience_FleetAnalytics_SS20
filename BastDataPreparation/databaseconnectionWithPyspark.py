'''
    This python file shows 2 different ways of how to connect a pyspark context
    with an mysql server and load data from it.
'''

# ---------------------------------- databaseconnectionWithPyspark ------------------------------------

#  Imports
from pyspark.sql import SQLContext
from pyspark import SparkContext

#  set SparkContext
sc = SparkContext()
sqlContext = SQLContext(sc)

#  set variables
hostname = "database-3.cpysja5lud5h.us-east-1.rds.amazonaws.com"
dbname = "fleetanalytics"
jdbcPort = 3306
username = "admin"
password = "fleetanalytics"

# ----------------------------------------- option 1 ----------------------------------
jdbcUrl = "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)
connectionProperties = {"user" : username,
                        "password" : password,
                        "driver" : "com.mysql.jdbc.Driver"}

df = sqlContext.read.jdbc(url=jdbcUrl, table='lkw_agg2', properties=connectionProperties)
df.show(n=20)

# ------------------------------------------ option 2 ----------------------------------
df = sqlContext.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://{0}:{1}/{2}".format(hostname, jdbcPort, dbname)) \
    .option("dbtable", "lkw_agg2") \
    .option("user", "admin") \
    .option("password", "fleetanalytics") \
    .load()

df.show(n=20)