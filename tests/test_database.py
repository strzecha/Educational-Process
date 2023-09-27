import pytest
import os

from utils.database import (
    create_connection, create_language_task_table, create_math_task_table,
    get_number_of_tables, insert_language_task, insert_math_task,
    select_data_by_id, select_all_data, update_language_task, update_math_task,
    count_total_correct, count_total_occurs
)
from utils.data_reader import get_properties

properties = get_properties()
DB_TEST_FILE = properties.get("TASKS_DB_TEST_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

@pytest.fixture(scope="module")
def connect():
    connection = create_connection(DB_TEST_FILE)
    yield locals()
    
    # close and remove database after all tests
    connection.close()  
    os.remove(DB_TEST_FILE)

def test_create_connection(connect):
    connection = connect['connection']
    assert connection is not None

def test_create_tables(connect):
    connection = connect['connection']
    create_language_task_table(connection)
    create_math_task_table(connection)

    assert get_number_of_tables(connection)[0] == 2

def test_insert_tables(connect):
    connection = connect['connection']

    words = [
        ["kot", "cat"],
        ["pies", "dog"],
        ["ptak", "bird"]
    ]
    for i in range(3):
        id = insert_language_task(connection, words[i])
        assert id == i + 1

    operators = ["+", "-"]
    for i in range(len(operators)):
        id = insert_math_task(connection, operators[i])
        assert id == i + 1

def test_select_all_data(connect):
    connection = connect['connection']

    rows = select_all_data(connection, LANGUAGE_TASKS_TABLE_NAME)
    assert len(rows) == 3

    rows = select_all_data(connection, MATH_TASKS_TABLE_NAME)
    assert len(rows) == 2

def test_select_data_by_id(connect):
    connection = connect['connection']

    row = select_data_by_id(connection, LANGUAGE_TASKS_TABLE_NAME, 2)
    assert row == (2, "pies", "dog", 0, 0)

    row = select_data_by_id(connection, MATH_TASKS_TABLE_NAME, 1)
    assert row == (1, "+", 0, 0)

def test_update_data(connect):
    connection = connect['connection']

    update_math_task(connection, 2, 1)
    update_math_task(connection, 2, 1)
    update_math_task(connection, 2, 0)

    row = select_data_by_id(connection, MATH_TASKS_TABLE_NAME, 2)

    assert row[2] == 3
    assert row[3] == 2

    update_language_task(connection, 1, 0)
    update_language_task(connection, 1, 1)
    update_language_task(connection, 1, 0)

    row = select_data_by_id(connection, LANGUAGE_TASKS_TABLE_NAME, 1)

    assert row[3] == 3
    assert row[4] == 1

def test_count_total_occurs(connect):
    connection = connect['connection']

    update_math_task(connection, 1, 1)
    update_math_task(connection, 1, 1)
    update_math_task(connection, 1, 0)

    num = count_total_occurs(connection, MATH_TASKS_TABLE_NAME)

    assert num == 6

def test_count_total_correct(connect):
    connection = connect['connection']

    update_language_task(connection, 1, 0)
    update_language_task(connection, 1, 1)

    num = count_total_correct(connection, LANGUAGE_TASKS_TABLE_NAME)

    assert num == 2