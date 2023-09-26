import sqlite3
from sqlite3 import Error

from utils.data_reader import get_properties

properties = get_properties()

DB_FILE = properties.get("TASKS_DB_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

def create_connection(db_file=DB_FILE):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return connection

def create_math_task_table(connection):
    sql = f"""
            CREATE TABLE IF NOT EXISTS {MATH_TASKS_TABLE_NAME} (
                id integer PRIMARY KEY,
                operator text NOT NULL,
                occurs_number integer DEFAULT 0,
                correct_number integer DEFAULT 0
            );
        """
    try:
        c = connection.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_language_task_table(connection):
    sql = f"""
            CREATE TABLE IF NOT EXISTS {LANGUAGE_TASKS_TABLE_NAME} (
                id integer PRIMARY KEY,
                word text NOT NULL,
                translation text NOT NULL,
                occurs_number integer DEFAULT 0,
                correct_number integer DEFAULT 0
            );
        """
    try:
        c = connection.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def update_language_task(connection, id, correct):
    row = select_data_by_id(connection, LANGUAGE_TASKS_TABLE_NAME, id)

    sql = f''' UPDATE {LANGUAGE_TASKS_TABLE_NAME}
              SET occurs_number = ? ,
                  correct_number = ?
              WHERE id = {id}'''
    
    cur = connection.cursor()
    cur.execute(sql, [row[3] + 1, row[4] + correct])
    connection.commit()

def update_math_task(connection, id, correct):
    row = select_data_by_id(connection, MATH_TASKS_TABLE_NAME, id)

    sql = f''' UPDATE {MATH_TASKS_TABLE_NAME}
              SET occurs_number = ? ,
                  correct_number = ?
              WHERE id = {id}'''
    
    cur = connection.cursor()
    cur.execute(sql, [row[2] + 1, row[3] + correct])
    connection.commit()

def insert_language_task(connection, data):
    sql = f"INSERT INTO {LANGUAGE_TASKS_TABLE_NAME}(word, translation) VALUES(?,?)"
    cur = connection.cursor()
    cur.execute(sql, data)
    connection.commit()

    return cur.lastrowid

def insert_math_task(connection, data):
    sql = f"INSERT INTO {MATH_TASKS_TABLE_NAME}(operator) VALUES(?)"
    cur = connection.cursor()
    cur.execute(sql, data)
    connection.commit()

    return cur.lastrowid

def select_data_by_id(connection, table_name, id):
    cur = connection.cursor()
    cur.execute(f"SELECT * FROM {table_name} WHERE id = {id}")

    row = cur.fetchone()

    return row

def get_number_of_tables(connection):
    sql = """
        SELECT count(*) 
        FROM sqlite_master 
        WHERE type = 'table' AND name != 'android_metadata' AND name != 'sqlite_sequence'
    """

    cur = connection.cursor()
    cur.execute(sql)

    row = cur.fetchone()

    return row

def select_all_data(connection, table_name):
    cur = connection.cursor()
    cur.execute(f"SELECT * FROM {table_name}")

    rows = cur.fetchall()

    return rows