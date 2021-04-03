'''
    This python file prepares the dash figure and cluster-specific dataframes
    for the final dashapp (Vizualisation). A histogram and a boxplot are built
    to show which trips are below and above a CO limit. Besides a line chart
    shows the linear regression between CO and fuel.

'''
# ---------------------------- emission -----------------------

# Imports
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go

# Get data from database
from Dashboard import databaseconnection

# ---------------------------- emission: histogram -----------------------

# Read data for histogram
df_hist = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

# Calculate how many data values are greater than 2500
l = len(df_hist.index)
i = 0
for index, row in df_hist.iterrows():
    if row['COperKM'] > 2500:
        i = i + 1

j = (i / l) * 100

# Histogram to show CO data per KM
a = df_hist["COperKM"]
fig_hist = go.Figure(data=[go.Histogram(x=a)])

fig_hist = px.histogram(df_hist, x="COperKM",
                        color_discrete_sequence=['#026fc8']  # color of histogram bars
                        )

# Adjust layout of the histogram
fig_hist.update_layout(
    xaxis_title="CO Austoß in mg/km",
    yaxis_title="Häufigkeit",
)

# Create line
fig_hist.add_trace(go.Scatter(
    x=[2500, 2500],
    y=[0, 160],
    mode="lines+markers",
    name="CO Grenzwert",

))

# ---------------------------- emission: boxplot -----------------------

# Read data for boxplot
df_box = pd.read_sql(
    'SELECT agg.COperKM from fleetanalytics.agg WHERE agg.COperKM<5000 '
    'LIMIT 50000;', con=databaseconnection.Connection.db_connection)

emissionBoxPlotTitle = "Schadstoffgrenze überschritten"

# Create boxplot
fig_box = px.box(df_box, y="COperKM", color_discrete_sequence=['#026fc8'])

# Create line
fig_box.add_shape(
    dict(
        type="line",
        x0=-1,
        y0=2500,
        x1=1,
        y1=2500,
        line=dict(
            color="red",
            width=3

        )
    )
)
# Create line
fig_box.add_trace(go.Scatter(
    x=[0, 0],
    y=[2500, 2500],
    mode="lines+markers",
    name="CO Grenzwert",

))

# Adjust layout of the boxplot
fig_box.update_layout(
    yaxis_title="CO Austoß in mg/km")

# ---------------------------- emission: line chart -----------------------

# Read data for line chart
df_line = pd.read_sql(
    'SELECT emissions.fuelKM, emissions.COKM from fleetanalytics.emissions '
    'LIMIT 90000;', con=databaseconnection.Connection.db_connection)

# linear regression to predict CO
x1 = df_line[['fuelKM']]
y1 = df_line[['COKM']]
model = LinearRegression()
model.fit(x1, y1)

# Build line chart
fig_line = px.line(df_line, y="COKM", x="fuelKM", color_discrete_sequence=['#026fc8'])

# Adjust laxout of the line chart
fig_line.update_layout(
    xaxis_title="Spritverbrauch in ml/km",
    yaxis_title="CO in mg/km")

# Create line
fig_line.add_trace(go.Scatter(
    x=[0, 2000],
    y=[2500, 2500],
    mode="lines+markers",
    name="CO Grenzwert",

))