import os
import logging
import psycopg2
import configparser
import pandas as pd

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from postgres_utils import get_postgres_config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = dash.Dash(__name__)
server = app.server


def read_all_weight_data():
    home = os.path.expanduser('~')
    postgres_args = get_postgres_config()
    query = "SELECT * FROM WEIGHT;"
    with psycopg2.connect(**postgres_args) as conn:
        df = pd.read_sql(query, conn)
    return df


def process_weight_data(df):
    df.drop('datetime', inplace=True, axis='columns')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['time'] = df['timestamp'].dt.time
    df['7-pt-MA'] = df['loss'].rolling(7).mean()
    return df


def get_month_start_loss(df):
    month_start_loss = (df
                        .set_index('timestamp')
                        .groupby(pd.Grouper(freq='MS'))
                        .last())
    month_start_loss = month_start_loss.reset_index()[['timestamp', 'loss']]
    month_start_loss['Month loss'] = (month_start_loss['loss']
                                      .diff()
                                      .fillna(month_start_loss['loss'])
                                      .round(2))
    month_start_loss = month_start_loss.reset_index()[['timestamp', 'Month loss']]
    month_start_loss['timestamp'] = month_start_loss['timestamp'].map(lambda t: t.strftime(format="%b-%y"))
    month_start_loss.rename(columns={'timestamp': 'Month'}, inplace=True)
    return month_start_loss


logging.info(f"Reading data from database")
df = process_weight_data(read_all_weight_data())
logging.info(f"Data obtained. Rows: {len(df)}")
month_start_loss = get_month_start_loss(df)
print(f"month_start_loss: {month_start_loss}")

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
        'text': f'<b>Total weighings = {len(df)}</b>',
        'y': 0.9,
        'x': 0.5,
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
    {
        'x': df['timestamp'].dt.hour + df['timestamp'].dt.minute/60,
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
        'text': '<b>Weighing hour of day</b>',
        'y': 0.9,
        'x': 0.5,
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


app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
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
        ], className="six columns", style={"height": "25%", "width": "50%", "margin": "auto"}),

        html.Div([
            dash_table.DataTable(
                data=month_start_loss.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in month_start_loss.columns],
                style_header={'backgroundColor': '#000000'},
                style_cell={
                    'backgroundColor': '#000000',
                    'color': '#7FDBFF'
                },
            )
        ], className="six columns", style={"height": "25%", "width": "25%", "margin": "auto"}),
    ], className="row")
])

if __name__ == "__main__":
    logging.info(f"Starting server..")
    app.run_server(host='0.0.0.0', debug=True)
