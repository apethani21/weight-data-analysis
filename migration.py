import os
import logging
import psycopg2
import configparser
import pandas as pd
import numpy as np
from gspread import Client

from api_handler import get_service_account_credentials
from postgres_utils import get_postgres_config, pgquery

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

col_name_mapper = {
    "Timestamp": "timestamp",
    "Datetime": "datetime",
    "Weight (KG)": "weight",
    "Loss (KG)": "loss"
}


def get_all_weight_data():
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    service_account_credentials = get_service_account_credentials(scopes)
    gc = Client(service_account_credentials)
    weight_track_spreadsheet = gc.open("weight-track").sheet1
    return weight_track_spreadsheet.get_all_records()


def upload_all():
    data = get_all_weight_data()
    logging.info("Data downloaded from sheet")
    df = pd.DataFrame(data)
    df.rename(columns=col_name_mapper, inplace=True)
    df = df[list(col_name_mapper.values())]
    data = df.to_records(index=False)
    query = "INSERT INTO WEIGHT VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING;"
    log_msg = "Writing data to database"
    pgquery(query, log_msg, data)
    postgres_config = get_postgres_config()
    logging.info(f"Migration completed successfully. {len(df)} rows.")
    return


if __name__ == "__main__":
    upload_all()
