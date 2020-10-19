import os
import logging
import psycopg2
import configparser
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from postgres_utils import get_postgres_config

sns.set_theme(rc={
                  'axes.axisbelow': False,
                  'axes.edgecolor': 'lightgrey',
                  'axes.facecolor': 'white',
                  'axes.grid': True,
                  'axes.titlesize': 18,
                  'grid.color': 'lightgrey',
                  'axes.labelcolor': 'dimgrey',
                  'axes.spines.right': False,
                  'axes.spines.top': False,
                  'figure.facecolor': 'white',
                  'lines.solid_capstyle': 'round',
                  'text.color': 'dimgrey',
                  'xtick.bottom': False,
                  'xtick.color': 'dimgrey',
                  'xtick.direction': 'out',
                  'xtick.labelsize': 15,
                  'xtick.top': False,
                  'ytick.color': 'dimgrey',
                  'ytick.labelsize': 15,
              })

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_all_weight_data():
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


def time_dist_plot(df, bins=8):
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    hours = df['timestamp'].dt.hour + df['timestamp'].dt.minute/60
    hours.name = "Hour of day"
    ax.hist(hours, bins=bins, color="#47DBCD", ec="none")
    ax.grid(False)
    ax.set_title("Hour of day when weighed", fontsize=15)
    return fig


def weight_loss_plot(df):
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    ax.plot(df['timestamp'], df['loss'],
            label='Loss (KG)',
            marker="o",
            markersize=10,
            color="#016794",
            linewidth=3,
            zorder=10)
    ax.plot(df['timestamp'], df['7-pt-MA'],
            label="7-point MA",
            color="crimson",
            alpha=0.75,
            linewidth=2,
            zorder=10)
    ax.legend(bbox_to_anchor=[0.98, 0.2])
    curr_loss = df.iloc[-1]['loss']
    ax.hlines(curr_loss,
              xmin=df['timestamp'].min(),
              xmax=df['timestamp'].max(),
              linewidth=2.5,
              colors="#F5AC4C",
              linestyles='--',
              label=str(curr_loss),
              zorder=10)
    ax.text(x=df['timestamp'].max(),
            y=curr_loss*1.05,
            s=f"{curr_loss}",
            size=15);
    ax.set_title(f"Total weighings: {len(df)}", fontsize=30)
    ax.tick_params(axis="x", rotation=30)
    return fig


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

st.title("Weight loss analysis")

wl_fig = weight_loss_plot(df)
time_dist_fig = time_dist_plot(df, bins=14)

st.pyplot(wl_fig)
col1, col2 = st.beta_columns([2, 1])
with col1:
    st.pyplot(time_dist_fig)
with col2:
    st.table(month_start_loss.set_index("Month").round(1).astype(str))
