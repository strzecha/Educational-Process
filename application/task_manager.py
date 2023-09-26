import random

from application.task import Task
from utils.data_reader import get_properties
from utils.database import select_all_data, create_connection

properties = get_properties()

NUM_TASKS = int(properties.get("NUM_TASKS").data)

ADD_RANGE = list(int(num) for num in properties.get("ADD_RANGE").data.split(","))
SUB_RANGE = list(int(num) for num in properties.get("SUB_RANGE").data.split(","))
MUL_RANGE = list(int(num) for num in properties.get("MUL_RANGE").data.split(","))
DIV_RANGE = list(int(num) for num in properties.get("DIV_RANGE").data.split(","))

LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data

class TaskManager:
    def __init__(self):
        self.add_range = ADD_RANGE
        self.sub_range = SUB_RANGE
        self.mul_range = MUL_RANGE
        self.div_range = DIV_RANGE

        self.language_tasks = None

    def generate_tasks(self):
        tasks = list()
        self.num = random.randint(0, 1)

        connection = create_connection()
        if connection:
            if self.num == 0: # math tasks
                self.math_tasks = select_all_data(connection, MATH_TASKS_TABLE_NAME)
            if self.num == 1: # language tasks
                self.language_tasks = select_all_data(connection, LANGUAGE_TASKS_TABLE_NAME)
            connection.close()
                
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
        operator_id, operator, occurs_num, correct_num = random.choice(self.math_tasks)

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
        
        question = f"{num1} {operator} {num2}"
        solution = int(eval(question))
        
        return Task(operator_id, question, solution, occurs_num, correct_num)

    def generate_foreign_language_task(self):
        id, word, translation, occurs_num, correct_num = random.choice(self.language_tasks)

        return Task(id, word, translation, occurs_num, correct_num)