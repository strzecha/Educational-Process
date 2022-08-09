import random

from task import MathTask, ForeignLanguageTask

OPERATORS = ["+", "-", "*", "/"]
NUM_TASKS = 10

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
            num1 = random.randint(0, 100)
            num2 = random.randint(0, 100 - num1)
        elif operator == "-":
            num1 = random.randint(0, 100)
            num2 = random.randint(0, num1)
        elif operator == "*":
            num1 = random.randint(0, 10)
            num2 = random.randint(0, 10)
        elif operator == "/":
            num2 = random.randint(1, 10)
            num1 = random.randint(0, 10) * num2

        return MathTask(num1, num2, operator)

    def generate_foreign_language_task(self):
        word = random.choice(list(FOREING_WORDS.keys()))
        translation = FOREING_WORDS[word]

        return ForeignLanguageTask(word, translation)