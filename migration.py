import os
import logging
import sqlite3
import pandas as pd
from gspread import Client
from api_handler import create_assertion_session

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    session = create_assertion_session(scopes)
    gc = Client(None, session)
    weight_track_spreadsheet = gc.open("weight-track").sheet1
    return weight_track_spreadsheet.get_all_records()


def upload_all():
    data = get_all_weight_data()
    logging.info("Data downloaded from sheet")
    df = pd.DataFrame(data)
    df.rename(columns=col_name_mapper, inplace=True)
    df = df[list(col_name_mapper.values())]
    home = os.path.expanduser('~')
    db = f"{home}/db/weight-data.db"
    with sqlite3.connect(db) as conn:
        logging.info("Writing data to database")
        df.to_sql('WEIGHT', conn, if_exists="replace", index=False)
    logging.info(f"Migration completed successfully. {len(df)} rows.")


if __name__ == "__main__":
    upload_all()
