import os
import sqlite3
import logging
import pandas as pd

import dash
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

main_chart_data = [
    {'x': df['timestamp'],
     'y': df['loss'],
     'type': 'scatter',
     'name': 'Loss (KG)',
     'mode': 'lines+markers',
     'marker': {'color': '#66B3FF'}},
    {'x': df['timestamp'],
     'y': df['7-pt-MA'].round(2),
     'type': 'scatter',
     'name': '7-point MA',
     'marker': {'color': '#FF447A'}},
     {'x': df['timestamp'],
      'y': [df['loss'].values[-1] for _ in range(len(df))],
      'type': 'scatter',
      'mode': 'line',
      'name': 'current',
      'marker': {'color': '#FFFF95'}}
]

main_chart_layout = {
                'plot_bgcolor': '#111111',
                'paper_bgcolor': '#111111',
                'font': {'color': '#7FDBFF'},
                'showlegend': True
            }

app.layout = html.Div(style={'backgroundColor': '#111111'}, children=[
    html.H1(
        children='Weight data analysis',
        style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }
    ),

    dcc.Graph(
        id='Weight loss',
        figure={
            'data': main_chart_data,
            'layout': main_chart_layout
        }
    )
])

logging.info(f"Starting server..")
app.run_server(debug=True)