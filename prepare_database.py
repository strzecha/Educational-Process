from utils.database import (create_connection, create_language_task_table, 
                            insert_language_task, select_all_data,
                            create_math_task_table, insert_math_task)
from utils.data_reader import get_properties

if __name__ == "__main__":

    properties = get_properties()
    connection = create_connection()

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
