import os
import logging
import sqlite3
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


def get_db_rows_count():
    home = os.path.expanduser('~')
    db = f"{home}/db/weight-data.db"
    query = "SELECT COUNT(timestamp) FROM WEIGHT;"
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        logging.info(f"Getting row count from {db}")
        cur.execute(query)
    return cur.fetchone()[0]


def get_new_weight_data():
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    number_of_rows = get_db_rows_count()
    session = create_assertion_session(scopes)
    gc = Client(None, session)
    weight_track_spreadsheet = gc.open("weight-track").sheet1
    row_count = number_of_rows + 2
    new_rows = []
    while True:
        logging.info(f"Getting row {row_count}")
        new_row = weight_track_spreadsheet.row_values(row_count)
        if len(new_row) == 0:
            logging.info(f"Row {row_count} not set")
            return new_rows
        else:
            new_rows.append(tuple(new_row))
            row_count += 1


def update_db():
    new_rows = get_new_weight_data()
    home = os.path.expanduser('~')
    db = f"{home}/db/weight-data.db"
    query = "INSERT INTO WEIGHT VALUES (?, ?, ?, ?);"
    logging.info(f"Inserting {len(new_rows)} new rows.")
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        logging.info(f"Getting row count from {db}")
        cur.executemany(query, new_rows)
    logging.info(f"Successfully updated db.")


if __name__ == "__main__":
    update_db()
