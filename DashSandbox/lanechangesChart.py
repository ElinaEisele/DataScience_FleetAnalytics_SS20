'''
    This python file creates a radar chart (spider web diagram) for the lanechange reasons.
    The attributes CO, speed, noise and fuel consumption are compared.
'''

# ----------------------------------------- Radar Chart of the lanechanges -------------------------------------------

# Imports
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# ---------------------------------------------- prepare data --------------------------------------

df = pd.DataFrame({
    'group': ['keepRight', 'speedGain', 'strategic', 'strategic_urgent', 'cooperative'],
    'speed': [111.27, 108.24, 96.77, 68.8, 26.8],
    'fuel': [14.08, 10.4, 17.41, 10.27,7.1],
    'CO': [39.87, 29.52, 49.1, 30.05,23.36],
    'noise': [86.58, 85.2, 85.06, 78.77,73.65],
})

# -------------------------------------------- prepare component ---------------------------------------

# ------- PART 1: Create background

# Number of variable
categories = list(df)[1:]
N = len(categories)

# What will be the angle of each axis in the plot?
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([25,50,75, 100], ["25","50","75", "100"], color="grey", size=7)
plt.ylim(0, 125)

# ------- PART 2: Add plots
# Plot each individual = each line of the data

# keepRight lanechange
values = df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="group keepRight")
ax.fill(angles, values, 'b', alpha=0.1)

# speedGain lanechange
values = df.loc[1].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="group speedGain")
ax.fill(angles, values, 'r', alpha=0.1)

# strategic lanechange
values = df.loc[2].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="group strategic")
ax.fill(angles, values, 'g', alpha=0.1)

# strategic_urgent lanechange
values = df.loc[3].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="group strategic_urgent")
ax.fill(angles, values, 'r', alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# Shows the chart
plt.show()