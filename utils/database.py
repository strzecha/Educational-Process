import sqlite3
from sqlite3 import Error

from utils.data_reader import get_properties

properties = get_properties()

DB_FILE = properties.get("TASKS_DB_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

OPERATORS = properties.get("MATH_OPERATORS").data.split(",")
FOREING_WORDS = {
        "kotwica": "anchor",
        "pies": "dog",
        "kot": "cat",
        "kropla": "drop",
        "pytanie": "question",
        "wykrzyknienie": "exclamation",
        "cel": "target",
        "znak": "sign",
        "ogień": "fire",
        "słońce": "sun",
        "księżyc": "moon",
        "kaktus": "cactus",
        "igloo": "igloo",
        "ptak": "bird",
        "kłódka": "padlock",
        "ołówek": "pencil",
        "wargi": "lips",
        "czaszka": "skull",
        "żarówka": "light bulb",
        "ser": "cheese",
        "pająk": "spider",
        "pajęczyna": "spider's web",
        "kostka lodu": "ice cube",
        "zielony": "green", 
        "drzewo": "tree", 
        "marchewka": "carrot",
        "serce": "heart",
        "klaun": "clown",
        "zebra": "zebra",
        "dinozaur": "dinosaur",
        "żółw": "turtle",
        "klucz wiolinowy": "clef",
        "klucz": "key",
        "zegar": "clock",
        "samochód": "car",
        "człowiek": "person",
        "delfin": "dolphin",
        "śnieżynka": "snowflake",
        "bałwan": "snowman",
        "jabłko": "apple",
        "duch": "ghost",
        "okulary": "glasses",
        "smok": "dragon",
        "oko": "eye",
        "nożyczki": "scissors",
        "bomba": "bomb",
        "biedronka": "ladybug",
        "piorun": "bolt",
        "liść": "leaf",
        "butelka": "bottle",
        "świeca": "candle",
        "młotek": "hammer",
        "kwiat": "flower",
        "koniczyna": "clover",
        "koń": "horse"
    }

def create_database(db_file=DB_FILE):
    connection = create_connection(db_file)
    if connection:
        create_language_task_table(connection)

        for key in FOREING_WORDS.keys():
            id = insert_language_task(connection, [key, FOREING_WORDS[key]])
        rows = select_all_data(connection, LANGUAGE_TASKS_TABLE_NAME)
        for row in rows:
            print(row)
        
        create_math_task_table(connection)
        for operator in OPERATORS:
            id = insert_math_task(connection, operator)
        rows = select_all_data(connection, MATH_TASKS_TABLE_NAME)
        for row in rows:
            print(row)

        connection.close()


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
    data = [row[3] + 1, row[4] + correct]

    do_query(connection, sql, data)

def update_math_task(connection, id, correct):
    row = select_data_by_id(connection, MATH_TASKS_TABLE_NAME, id)

    sql = f''' UPDATE {MATH_TASKS_TABLE_NAME}
              SET occurs_number = ? ,
                  correct_number = ?
              WHERE id = {id}'''
    data = [row[2] + 1, row[3] + correct]

    do_query(connection, sql, data)

def do_query(connection, sql, data):
    cur = connection.cursor()
    cur.execute(sql, data)
    connection.commit()

    return cur.lastrowid

def get_rows(connection, sql):
    cur = connection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    return rows

def insert_language_task(connection, data):
    sql = f"INSERT INTO {LANGUAGE_TASKS_TABLE_NAME}(word, translation) VALUES(?,?)"
    
    last_id = do_query(connection, sql, data)
    return last_id

def insert_math_task(connection, data):
    sql = f"INSERT INTO {MATH_TASKS_TABLE_NAME}(operator) VALUES(?)"

    last_id = do_query(connection, sql, data)
    return last_id

def select_data_by_id(connection, table_name, id):
    sql = f"SELECT * FROM {table_name} WHERE id = {id}"

    rows = get_rows(connection, sql)

    return rows[0]

def get_number_of_tables(connection):
    sql = """
        SELECT count(*) 
        FROM sqlite_master 
        WHERE type = 'table' AND name != 'android_metadata' AND name != 'sqlite_sequence'
    """

    rows = get_rows(connection, sql)

    return rows[0]

def select_all_data(connection, table_name):
    sql = f"SELECT * FROM {table_name}"

    rows = get_rows(connection, sql)

    return rows

def count_total_occurs(connection, table_name):
    sql = f"""
        SELECT SUM(occurs_number)
        FROM {table_name}
        """
    
    rows = get_rows(connection, sql)

    return int(rows[0][0])

def count_total_correct(connection, table_name):
    sql = f"""
        SELECT SUM(correct_number)
        FROM {table_name}   
        """

    rows = get_rows(connection, sql)

    return int(rows[0][0])
