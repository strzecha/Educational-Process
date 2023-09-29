from utils.database import create_database
from utils.data_reader import get_properties

if __name__ == "__main__":

    properties = get_properties()
    DB_FILE = properties.get("TASKS_DB_NAME").data
    WEEK_DB_FILE = properties.get("TASKS_WEEK_DB_NAME").data
    LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
    MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

    for db_name in {DB_FILE, WEEK_DB_FILE}:
        db = create_database(db_name)