"""Tests for data_reader module
"""

import pytest

from utils.data_reader import check_properties, get_properties, WrongPropertiesError

def test_check_properties():
    check_properties()

def test_check_wrong_properties():
    with pytest.raises(WrongPropertiesError):
        check_properties("tests/wrong_properties")

def test_get_properties():
    properties = get_properties()

    LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
    MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data
    TASKS_DB_NAME = properties.get("TASKS_DB_NAME").data

    assert LANGUAGE_TASKS_TABLE_NAME == "language_tasks"
    assert MATH_TASKS_TABLE_NAME == "math_tasks"
    assert TASKS_DB_NAME == "all_tasks.db"