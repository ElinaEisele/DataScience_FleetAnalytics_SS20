'''
  This python file reads the bast data (in hours) and transforms them into the
  required flow.csv file for the DFROUTER statement in the SUMO comandline using pyspark.
'''

# ---------------------------------- readBastDataWithPyspark -----------------------------------------------

# Imports
from datetime import datetime
from pyspark import SparkContext, SQLContext
import pyspark.sql.functions as F
from pyspark.sql.types import StringType, IntegerType, TimestampType, LongType

# set SparkContext
sc = SparkContext()
sql = SQLContext(sc)


# set path variables
path = 'C:\\Users\\elina\\Documents\\HdM\\Semester6\\Data_Science_Project\\SUMOProjekt\\germanyData\\'
input_A_S = path+'2018_A_S.txt'
input_B_S = path+'2018_B_S.txt'

# the output will be written in the following folder, a file name is not required
output = path+'flow'
bundesland = 11
startDatum = '180101'
startDatum = datetime.strptime(startDatum, '%y%m%d')

# --------------------------------------- Data Preperation --------------------------------------

# read csv files for higways and main roads
df_i_A = (sql.read.csv(input_A_S, header=True, sep=';'))
df_i_B = (sql.read.csv(input_B_S, header=True, sep=';'))

# filter by state --> optional
# df_i_A = df_i_A.filter(F.col('Land') == bundesland)
# df_i_B = df_i_B.filter(F.col('Land') == bundesland)

# select columns
df_i_A = df_i_A.select('Zst', 'Datum', 'Stunde', 'KFZ_R1', 'Lkw_R1')
df_i_B = df_i_B.select('Zst', 'Datum', 'Stunde', 'KFZ_R1', 'Lkw_R1')

# remove blanks
df_i_B = df_i_B.withColumn("KFZ_R1", F.trim(F.col("KFZ_R1")))
df_i_B = df_i_B.withColumn("Lkw_R1", F.trim(F.col("Lkw_R1")))

# unite motor highway and main road in one dataframe
df_AB = df_i_A.union(df_i_B)

# ------------------------------------- Data Transformation ----------------------------------

# subtract 1 to get the actual hours
df_AB = df_AB.withColumn('Stunde', df_AB['Stunde'].cast(IntegerType()))
df_AB = df_AB.withColumn('Stunde', F.col('Stunde') - 1)
df_AB = df_AB.withColumn('Stunde', df_AB['Stunde'].cast(StringType()))

# convert to timestamp format
df_AB = df_AB.withColumn('Time', F.concat(F.col('Datum'), F.lit(' '), F.col('Stunde')))
df_AB = df_AB.withColumn('Time', F.unix_timestamp('Time', "yyMMdd HH").cast(TimestampType()))

#  calculate past days since the beginning of the year
df_AB = df_AB.withColumn('StartDate', F.lit(startDatum))

# convert to minutes and save as an integer
df_AB_Time = df_AB.withColumn('DiffInSeconds',F.col('Time').cast(LongType()) - F.col('StartDate').cast(LongType()))\
  .withColumn('DiffInMinutes',(F.col('DiffInSeconds')/60))
df_AB_Time = df_AB_Time.withColumn('DiffInMinutes', df_AB_Time['DiffInMinutes'].cast(IntegerType()))

# remove, rename and add columns
df_AB_Time = df_AB_Time.drop('Time', 'StartDate', 'DiffInSeconds', 'Stunde', 'Datum')
df_AB_Time = df_AB_Time.withColumnRenamed('DiffInMinutes', 'Time')\
  .withColumnRenamed('Zst', 'Detector')\
  .withColumnRenamed('KFZ_R1', 'qPKW')\
  .withColumnRenamed('Lkw_R1', 'qLKW')
df_AB_Time = df_AB_Time.withColumn('vPKW', F.lit(100)).withColumn('vLKW', F.lit(80))

df_out = df_AB_Time.select('Detector', 'Time', 'qPKW', 'qLKW', 'vPKW', 'vLKW')

# df_out.show(n=30)
# print(df_out.count())

# write csv to output path
df_out.coalesce(1).write.csv(output, header=True)
