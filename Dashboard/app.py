"""
    Contains the app-Object needed for deployment
"""

import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Get Dash App Object
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Because we use tabs in the index file to build the site, the ids of the content don't exist when loading the page.
app.config['suppress_callback_exceptions'] = True

