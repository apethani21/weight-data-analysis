import os
import logging
import psycopg2
import configparser


def get_postgres_config():
    home = os.path.expanduser("~")
    path_to_config = f"{home}/postgres-config/config.ini"
    config = configparser.ConfigParser()
    config.read(path_to_config)
    return dict(config["postgres"])


def pgquery(query, log_msg=None, data=None):
    postgres_config = get_postgres_config()
    with psycopg2.connect(**postgres_config) as conn:
        cur = conn.cursor()
        logging.info(log_msg)
        if data is None:
            cur.execute(query)
        else:
            cur.executemany(query, data)
    return cur