import random

from task import MathTask, ForeignLanguageTask
from data_reader import get_properties

properties = get_properties()

OPERATORS = properties.get("MATH_OPERATORS").data.split(",")
NUM_TASKS = int(properties.get("NUM_TASKS").data)

ADD_RANGE = list(int(num) for num in properties.get("ADD_RANGE").data.split(","))
SUB_RANGE = list(int(num) for num in properties.get("SUB_RANGE").data.split(","))
MUL_RANGE = list(int(num) for num in properties.get("MUL_RANGE").data.split(","))
DIV_RANGE = list(int(num) for num in properties.get("DIV_RANGE").data.split(","))

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

class TaskManager:
    def __init__(self):
        self.add_range = ADD_RANGE
        self.sub_range = SUB_RANGE
        self.mul_range = MUL_RANGE
        self.div_range = DIV_RANGE

    def generate_tasks(self):
        tasks = list()
        self.num = random.randint(0, 1)

        for _ in range(NUM_TASKS):
            if self.num == 0:
                task = self.generate_math_task()
            elif self.num == 1:
                task = self.generate_foreign_language_task()

            tasks.append(task)

        return tasks

    def get_num(self):
        return self.num

    def generate_math_task(self):
        operator = random.choice(OPERATORS)

        if operator == "+":
            num1 = random.randint(*self.add_range)
            num2 = random.randint(*self.add_range)
        elif operator == "-":
            num1 = random.randint(*self.sub_range)
            num2 = random.randint(self.sub_range[0], num1)
        elif operator == "*":
            num1 = random.randint(*self.mul_range)
            num2 = random.randint(*self.mul_range)
        elif operator == "/":
            num2 = random.randint(*self.div_range)
            num2 = max(num2, 1)
            num1 = random.randint(*self.div_range) * num2

        return MathTask(num1, num2, operator)

    def generate_foreign_language_task(self):
        word = random.choice(list(FOREING_WORDS.keys()))
        translation = FOREING_WORDS[word]

        return ForeignLanguageTask(word, translation)