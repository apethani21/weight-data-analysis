import os
import sqlite3
import logging
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = dash.Dash(__name__)
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

loss_chart_data = [
    {'x': df['timestamp'],
     'y': df['loss'],
     'type': 'scatter',
     'name': 'Loss (KG)',
     'mode': 'lines+markers',
     'marker': {'color': '#7FDBFF', 'size': 6}},
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
      'marker': {'color': '#7FFFD4', 'line': {'width': 8}}}
]

loss_chart_layout = {
    'plot_bgcolor': '#000000',
    'paper_bgcolor': '#000000',
    'font': {'color': '#7FDBFF'},
    'showlegend': True,
    'title': {
        'text': f'Total weighings = {len(df)}',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    'xaxis': {
        'showline': True,
        'linecolor': '#7FDBFF',
        'showgrid': True,
        'gridcolor': '#7FDBFF',
        'linewidth': 3
    },
    'yaxis': {
        'showline': True,
        'linecolor': '#7FDBFF',
        'showgrid': True,
        'gridcolor': '#7FDBFF',
        'linewidth': 3
    }
 }

timing_chart_data = [
    {'x': df['timestamp'].dt.hour + df['timestamp'].dt.minute/60,
     'type': 'histogram',
     'name': 'Weighing time of day',
     'marker': {'color': '#7FDBFF'}
    }
]

timing_chart_layout = {
    'plot_bgcolor': '#000000',
    'paper_bgcolor': '#000000',
    'font': {'color': '#7FDBFF'},
    'showlegend': True,
    'title': {
        'text': 'Weighing hour of day',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    'xaxis': {
        'showline': True,
        'linecolor': '#7FDBFF',
        'showgrid': True,
        'gridcolor': '#7FDBFF',
        'linewidth': 3
    },
    'yaxis': {
        'showline': True,
        'linecolor': '#7FDBFF',
        'showgrid': True,
        'gridcolor': '#7FDBFF',
        'linewidth': 3
    }
}


app.layout = html.Div(style={'backgroundColor':'black'}, children=[
    html.Div([
        html.Div([
            dcc.Graph(
                id='Weight loss',
                figure={
                    'data': loss_chart_data,
                    'layout': loss_chart_layout
                },
            ),
        ], className="six columns"),

        html.Div([
            dcc.Graph(
                id='Weight time',
                figure={
                    'data': timing_chart_data,
                    'layout': timing_chart_layout
                }
    )
        ], className="six columns"),
    ], className="row")
])

logging.info(f"Starting server..")
app.run_server(host='0.0.0.0')
