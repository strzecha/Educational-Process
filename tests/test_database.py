import pytest
import os

from utils.database import TaskDatabase
from utils.data_reader import get_properties

properties = get_properties()
DB_TEST_FILE = properties.get("TASKS_DB_TEST_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

@pytest.fixture(scope="module")
def connect():
    db = TaskDatabase(DB_TEST_FILE)
    yield locals()
    
    # close and remove database after all tests
    db.close()  
    os.remove(DB_TEST_FILE)

def test_create_connection(connect):
    connection = connect['db'].connection
    assert connection is not None

def test_create_tables(connect):
    db = connect['db']
    db.create_language_task_table()
    db.create_math_task_table()

    assert db.get_number_of_tables()[0] == 2

def test_insert_tables(connect):
    db = connect['db']

    words = [
        ["kot", "cat"],
        ["pies", "dog"],
        ["ptak", "bird"]
    ]
    for i in range(3):
        id = db.insert_language_task(words[i])
        assert id == i + 1

    operators = ["+", "-"]
    for i in range(len(operators)):
        id = db.insert_math_task(operators[i])
        assert id == i + 1

def test_select_all_data(connect):
    db = connect['db']

    rows = db.select_all_data(LANGUAGE_TASKS_TABLE_NAME)
    assert len(rows) == 3

    rows = db.select_all_data(MATH_TASKS_TABLE_NAME)
    assert len(rows) == 2

def test_select_data_by_id(connect):
    db = connect['db']

    row = db.select_data_by_id(LANGUAGE_TASKS_TABLE_NAME, 2)
    assert row == (2, "pies", "dog", 0, 0)

    row = db.select_data_by_id(MATH_TASKS_TABLE_NAME, 1)
    assert row == (1, "+", 0, 0)

def test_update_data(connect):
    db = connect['db']

    db.update_math_task(2, 1)
    db.update_math_task(2, 1)
    db.update_math_task(2, 0)

    row = db.select_data_by_id(MATH_TASKS_TABLE_NAME, 2)

    assert row[2] == 3
    assert row[3] == 2

    db.update_language_task(1, 0)
    db.update_language_task(1, 1)
    db.update_language_task(1, 0)

    row = db.select_data_by_id(LANGUAGE_TASKS_TABLE_NAME, 1)

    assert row[3] == 3
    assert row[4] == 1

def test_count_total_occurs(connect):
    db = connect['db']

    db.update_math_task(1, 1)
    db.update_math_task(1, 1)
    db.update_math_task(1, 0)

    num = db.count_total_occurs(MATH_TASKS_TABLE_NAME)

    assert num == 6

def test_count_total_correct(connect):
    db = connect['db']

    db.update_language_task(1, 0)
    db.update_language_task(1, 1)

    num = db.count_total_correct(LANGUAGE_TASKS_TABLE_NAME)

    assert num == 2