import sqlite3
from sqlite3 import Error

from data_reader import get_properties

properties = get_properties()

DB_FILE = properties.get("TASKS_DB_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data

def create_connection():
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(DB_FILE)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return connection

def create_language_task_table(connection):
    sql = f"""
            CREATE TABLE IF NOT EXISTS {LANGUAGE_TASKS_TABLE_NAME} (
                id integer PRIMARY KEY,
                word text NOT NULL,
                translation text NOT NULL
            );
        """
    try:
        c = connection.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def insert_language_task(connection, data):
    sql = f"INSERT INTO {LANGUAGE_TASKS_TABLE_NAME}(word, translation) VALUES(?,?)"
    cur = connection.cursor()
    cur.execute(sql, data)
    connection.commit()

    return cur.lastrowid

def select_all_data(connection, table_name):
    cur = connection.cursor()
    cur.execute(f"SELECT * FROM {table_name}")

    rows = cur.fetchall()

    return rows