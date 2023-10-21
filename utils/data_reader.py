import csv
import os

from jproperties import Properties

class WrongPropertiesError(Exception):
    pass

def check_properties(file_name="properties"):
    configs = get_properties(file_name)
    
    DEBUG = configs.get("DEBUG").data
    if DEBUG.upper() not in ("TRUE", "FALSE"):
        raise WrongPropertiesError("DEBUG")
    
    DELAY = configs.get("DELAY").data
    try:
        DELAY = int(DELAY)
        if DELAY <= 0:
            raise WrongPropertiesError("DELAY")
    except:
        raise WrongPropertiesError("DELAY")


    for RANGE_NAME in ("ADD_RANGE", "SUB_RANGE", 
                  "MUL_RANGE", "DIV_RANGE"):
        
        RANGE = configs.get(RANGE_NAME).data
        RANGE = RANGE.split(',')
        if len(RANGE) != 2:
            raise WrongPropertiesError(RANGE_NAME)
        else:
            try:
                RANGE[0], RANGE[1] = int(RANGE[0]), int(RANGE[1])
                if RANGE[0] > RANGE[1]:
                    raise WrongPropertiesError(RANGE_NAME)
            except:
                raise WrongPropertiesError(RANGE_NAME)

    NUM_TASKS = configs.get("NUM_TASKS").data
    try:
        NUM_TASKS = int(NUM_TASKS)
        if NUM_TASKS <= 0:
            raise WrongPropertiesError("NUM_TASKS")
    except:
        raise WrongPropertiesError("NUM_TASKS")
    
    THRESHOLD = configs.get("THRESHOLD").data
    try:
        THRESHOLD = int(THRESHOLD)
        if THRESHOLD > NUM_TASKS:
            raise WrongPropertiesError("THRESHOLD")
    except:
        raise WrongPropertiesError("THRESHOLD")

    MATH_OPERATORS = configs.get("MATH_OPERATORS").data
    MATH_OPERATORS = MATH_OPERATORS.split(',')

    for OPERATOR in MATH_OPERATORS:
        try:
            eval(f"1{OPERATOR}1")
        except:
            raise WrongPropertiesError("MATH_OPERATORS")
        
    WORDS_FILES = configs.get("WORDS_FILES").data
    WORDS_FILES = WORDS_FILES.split(",")

    for WORDS_FILE in WORDS_FILES:
        if not os.path.exists(WORDS_FILE):
            raise WrongPropertiesError("WORDS_FILES")

    TASKS_DB_NAME = configs.get("TASKS_DB_NAME").data
    if not os.path.exists(TASKS_DB_NAME):
        raise WrongPropertiesError("TASKS_DB_NAME")
    
    TASKS_WEEK_DB_NAME = configs.get("TASKS_WEEK_DB_NAME").data
    if not os.path.exists(TASKS_WEEK_DB_NAME):
        raise WrongPropertiesError("TASKS_WEEK_DB_NAME")

    CREDENTIALS_FILE = configs.get("CREDENTIALS_FILE").data
    if not os.path.exists(CREDENTIALS_FILE):
        raise WrongPropertiesError("CREDENTIALS_FILE")

def get_properties(file_name="properties"):
    """Function to get properties from properties file

    Args:
        file_name (str, optional): name od properties file. Defaults to "properties".

    Returns:
        Properties: properties 
    """

    configs = Properties()
    with open(file_name, 'rb') as config_file:
        configs.load(config_file, encoding="utf-8")

    return configs

def read_data_words_from_file(filename):
    """Function to read data from csv file

    Args:
        filename (str): name of csv file

    Returns:
        list: data from file
    """
    
    results = list()
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', fieldnames=["word", "translation"])
        for row in reader:
            results.append(row)

    return results