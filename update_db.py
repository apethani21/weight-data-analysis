import os
import logging
import psycopg2
from gspread import Client

from api_handler import get_service_account_credentials
from postgres_utils import get_postgres_config, pgquery

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

col_name_mapper = {
    "Timestamp": "timestamp",
    "Datetime": "datetime",
    "Weight (KG)": "weight",
    "Loss (KG)": "loss"
}


def get_db_rows_count():
    postgres_config = get_postgres_config()
    query = "SELECT COUNT(timestamp) FROM WEIGHT;"
    log_msg = "Getting row count from WEIGHT database"
    cur = pgquery(query, log_msg)
    return cur.fetchone()[0]


def get_new_weight_data():
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    number_of_rows = get_db_rows_count()
    service_account_credentials = get_service_account_credentials(scopes)
    gc = Client(service_account_credentials)
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
    if not new_rows:
        logging.info("No new rows to add.")
        return
    query = "INSERT INTO WEIGHT VALUES (%s, %s, %s, %s);"
    log_msg = f"Inserting {len(new_rows)} new rows."
    pgquery(query, log_msg, new_rows)
    logging.info(f"Successfully updated WEIGHT database.")
    return


if __name__ == "__main__":
    update_db()
