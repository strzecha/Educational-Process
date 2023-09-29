from utils.database import create_database, TaskDatabase
from utils.data_reader import get_properties

if __name__ == "__main__":

    properties = get_properties()
    DB_FILE = properties.get("TASKS_DB_NAME").data
    WEEK_DB_FILE = properties.get("TASKS_WEEK_DB_NAME").data
    LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
    MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

    for db_name in {DB_FILE, WEEK_DB_FILE}:
        db = create_database(db_name)

        """if connection:
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

            connection.close()"""
