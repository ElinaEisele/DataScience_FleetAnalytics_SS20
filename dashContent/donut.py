'''
    This python file prepares the dash figures and dataframes
    for the final dashapp (Vizualisation). A donut diagram is
    created to show the percentage of trips that overrun a CO
    limit. Besides a donut diagram is created to show the weekly
    driving time of the drivers.


'''
# ---------------------------- donut -----------------------

import plotly.graph_objects as go
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from Dashboard.dashContent import emission


# ---------------------------- donut: percentage exceeded limit -----------------------

labels = ['Fahrten mit CO-Wert unter Grenzwert', 'Fahrten mit zu hohem CO-Wert']
values = [round(emission.j, 2), round(100-emission.j, 2)]

colors = ['#ef553b', '#026fc8']

donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8, textinfo="none")])

# Add Text in the Middle, adjust size
donut.update_layout(
                    autosize=False,
                    height=140,
                    width=850, margin=dict(t=20, b=20, l=20, r=20)
                    )

donut.update_traces(marker=dict(colors=colors))

# ---------------------------- donut: driving time per week -----------------------

# Add Text in the Middle, adjust size

labels = ['Ausschöpfung der wöchentlichen Lenkzeit in %', 'Noch verfügbare wöchentliche Lenkzeit in %']

values1 = [85, 15]
donut1 = go.Figure(data=[go.Pie(labels=labels, values=values1, hole=.8, textinfo="none")])
donut1.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut1.update_traces(marker=dict(colors=colors))

values2 = [95, 5]
donut2 = go.Figure(data=[go.Pie(labels=labels, values=values2, hole=.8, textinfo="none")])
donut2.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut2.update_traces(marker=dict(colors=colors))

values3 = [69, 31]
donut3 = go.Figure(data=[go.Pie(labels=labels, values=values3, hole=.8, textinfo="none")])
donut3.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut3.update_traces(marker=dict(colors=colors))

values4 = [18, 82]
donut4 = go.Figure(data=[go.Pie(labels=labels, values=values4, hole=.8, textinfo="none")])
donut4.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut4.update_traces(marker=dict(colors=colors))

values5 = [100, 0]
donut5 = go.Figure(data=[go.Pie(labels=labels, values=values5, hole=.8, textinfo="none")])
donut5.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut5.update_traces(marker=dict(colors=colors))

values6 = [91, 9]
donut6 = go.Figure(data=[go.Pie(labels=labels, values=values6, hole=.8, textinfo="none")])
donut6.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut6.update_traces(marker=dict(colors=colors))

values7 = [87, 13]
donut7 = go.Figure(data=[go.Pie(labels=labels, values=values7, hole=.8, textinfo="none")])
donut7.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut7.update_traces(marker=dict(colors=colors))

values8 = [97, 3]
donut8 = go.Figure(data=[go.Pie(labels=labels, values=values8, hole=.8, textinfo="none")])
donut8.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut8.update_traces(marker=dict(colors=colors))

values9 = [77, 23]
donut9 = go.Figure(data=[go.Pie(labels=labels, values=values9, hole=.8, textinfo="none")])
donut9.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut9.update_traces(marker=dict(colors=colors))

values10 = [99, 1]
donut10 = go.Figure(data=[go.Pie(labels=labels, values=values10, hole=.8, textinfo="none")])
donut10.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut10.update_traces(marker=dict(colors=colors))

values11 = [98, 2]
donut11 = go.Figure(data=[go.Pie(labels=labels, values=values11, hole=.8, textinfo="none")])
donut11.update_layout(autosize=False, height=150, width=850, margin=dict(t=20, b=20, l=20, r=20))
donut11.update_traces(marker=dict(colors=colors))
