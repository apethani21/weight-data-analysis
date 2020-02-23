import os
import sqlite3
import logging
import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets)
server = app.server

def read_all_weight_data():
    home = os.path.expanduser('~')
    db = f"{home}/db/weight-data.db"
    query = "SELECT * FROM WEIGHT"
    with sqlite3.connect(db) as conn:
        df = pd.read_sql(query, conn)
    return df

def process_weight_data(df):
    df.drop('datetime', inplace=True, axis='columns')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['time'] = df['timestamp'].dt.time
    df['7-pt-MA'] = df['loss'].rolling(7).mean()
    return df

logging.info(f"Reading data from database")
df = process_weight_data(read_all_weight_data())

logging.info(f"Data obtained. Rows: {len(df)}")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Weight data analysis',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='Weight loss',
        figure={
            'data': [
                {'x': df['timestamp'], 'y': df['loss'], 'type': 'scatter', 'name': 'Weight loss'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])


logging.info(f"Starting server..")
app.run_server(debug=True)