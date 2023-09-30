import sqlite3
from sqlite3 import Error

from utils.data_reader import get_properties, read_data_words_from_file
from datatypes  .task import Task, MathTask

properties = get_properties()

DB_FILE = properties.get("TASKS_DB_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

OPERATORS = properties.get("MATH_OPERATORS").data.split(",")
WORDS_FILES = properties.get("WORDS_FILES").data.split(",")

class TaskDatabase:
    """class TaskDatabase

    Class to representation of database with tasks
    """

    def __init__(self, db_file=DB_FILE):
        """Init method

        Args:
            db_file (str, optional): name of file with database
        """

        self.db_file = db_file
        self.connection = None

        self.create_connection()

    def create_connection(self):
        """Method to create a database connection to a SQLite database
        """

        try:
            self.connection = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)

    def create_math_task_table(self):
        """Method to create table with math tasks in database
        """
        
        sql = f"""
            CREATE TABLE IF NOT EXISTS {MATH_TASKS_TABLE_NAME} (
                id integer PRIMARY KEY,
                operator text NOT NULL,
                occurs_number integer DEFAULT 0,
                correct_number integer DEFAULT 0
            );
        """
        try:
            c = self.connection.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def create_language_task_table(self):
        """Method to create table with language tasks in database
        """

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
            c = self.connection.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def update_language_task(self, id, correct):
        """Method to updated table with language tasks in database

        Args:
            id (int): id of updated task
            correct (int, {0, 1}): number of correct aswers to updated task
        """

        row = self.get_task_by_id(LANGUAGE_TASKS_TABLE_NAME, id)

        sql = f''' UPDATE {LANGUAGE_TASKS_TABLE_NAME}
                SET occurs_number = ? ,
                    correct_number = ?
                WHERE id = {id}'''
        data = [row[3] + 1, row[4] + correct]

        self.do_query(sql, data)

    def update_math_task(self, id, correct):
        """Method to updated table with math tasks in database

        Args:
            id (int): id of updated task
            correct (int, {0, 1}): number of correct aswers to updated task
        """

        row = self.get_task_by_id(MATH_TASKS_TABLE_NAME, id)

        sql = f''' UPDATE {MATH_TASKS_TABLE_NAME}
                SET occurs_number = ? ,
                    correct_number = ?
                WHERE id = {id}'''
        data = [row[2] + 1, row[3] + correct]

        self.do_query(sql, data)

    def do_query(self, sql, data):
        """Method to perform query which using additional data

        Args:
            sql (str): contents of query
            data (list): data 

        Returns:
            int: ID of last updated/added row
        """

        cur = self.connection.cursor()
        cur.execute(sql, data)
        self.connection.commit()

        return cur.lastrowid

    def get_rows(self, sql):
        """Method to get rows from database

        Args:
            sql (str): contents of query

        Returns:
            list: contents of chosen rows
        """

        cur = self.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return rows

    def insert_language_task(self, data):
        """Method to insert new task to table with language tasks in database

        Args:
            data (list): data
        
        Returns:
            int: id of inserted task
        """

        sql = f"INSERT INTO {LANGUAGE_TASKS_TABLE_NAME}(word, translation) VALUES(?,?)"
        
        id = self.do_query(sql, data)
        return id

    def insert_math_task(self, data):
        """Method to insert new task to table with math tasks in database

        Args:
            data (list): data
        
        Returns:
            int: id of inserted task
        """

        sql = f"INSERT INTO {MATH_TASKS_TABLE_NAME}(operator) VALUES(?)"

        last_id = self.do_query(sql, data)
        return last_id

    def get_task_by_id(self, table_name, id):
        """Method to get task with given ID

        Args:
            table_name (str): name of table
            id (ind): id of task
        
        Returns:
            list: chosen task
        """

        sql = f"SELECT * FROM {table_name} WHERE id = {id}"

        rows = self.get_rows(sql)

        return rows[0]

    def get_number_of_tables(self):
        """Method to get number of tables in database
        
        Returns:
            int: number of tables
        """

        sql = """
            SELECT count(*) 
            FROM sqlite_master 
            WHERE type = 'table' AND name != 'android_metadata' AND name != 'sqlite_sequence'
        """

        rows = self.get_rows(sql)

        return rows[0][0]

    def select_all_data(self, table_name):
        """Method to get all data from given table 

        Args:
            table_name (str): name of chosen table
        
        Returns:
            list: data from table
        """

        sql = f"SELECT * FROM {table_name}"

        rows = self.get_rows(sql)

        return rows
    
    def get_all_math_tasks(self):
        """Method to get all math tasks from database

        Returns:
            list: all math tasks
        """

        rows = self.select_all_data(MATH_TASKS_TABLE_NAME)

        tasks = list()

        for row in rows:
            task = MathTask(*row)
            tasks.append(task)

        return tasks
    
    def get_all_language_tasks(self):
        """Method to get all language tasks from database
        
        Returns:
            list: all language tasks
        """

        rows = self.select_all_data(LANGUAGE_TASKS_TABLE_NAME)

        tasks = list()

        for row in rows:
            task = Task(*row)
            tasks.append(task)

        return tasks

    def count_total_occurs(self, table_name):
        """Method to count all occurs of all tasks from chosen table

        Args:
            table_name (str): name of chosen table
        
        Returns:
            int: number of occurs of all tasks 
        """

        sql = f"""
            SELECT SUM(occurs_number)
            FROM {table_name}
            """
        
        rows = self.get_rows(sql)

        return int(rows[0][0])

    def count_total_correct(self, table_name):
        """Method to count all correct answers to tasks from chosen table
        Args:
            table_name (str): name of chosen table
        
        Returns:
            int: number of correct answers to all tasks
        """

        sql = f"""
            SELECT SUM(correct_number)
            FROM {table_name}   
            """

        rows = self.get_rows(sql)

        return int(rows[0][0])

    def close(self):
        """Method to close connection with database
        """

        self.connection.close()


def create_database(db_file=DB_FILE):
    """Function to create database with default data
    """

    db = TaskDatabase(db_file)
    if db.connection:
        db.create_language_task_table()

        for filename in WORDS_FILES:
            data = read_data_words_from_file(filename)
            for row in data:
                db.insert_language_task([row["word"], row["translation"]])
        
        db.create_math_task_table()
        for operator in OPERATORS:
            id = db.insert_math_task(operator)

        db.close()
