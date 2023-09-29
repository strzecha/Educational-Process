import random
import numpy.random as nprand

from application.task import Task
from utils.data_reader import get_properties
from utils.database import TaskDatabase

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
        self.number_of_tasks = NUM_TASKS

    def generate_tasks(self):
        tasks = list()
        self.num = random.randint(0, 1)

        db = TaskDatabase()
        if db.connection:
            if self.num == 0: # math tasks
                self.math_tasks = db.select_all_data(MATH_TASKS_TABLE_NAME)
            if self.num == 1: # language tasks
                self.language_tasks = db.select_all_data(LANGUAGE_TASKS_TABLE_NAME)
            db.close()
                

        if self.num == 0:
            tasks = self.generate_math_tasks()
        elif self.num == 1:
            tasks = self.generate_foreign_language_tasks()

        return tasks

    def get_num(self):
        return self.num

    def generate_math_tasks(self):
        tasks = list()
        for i in range(self.number_of_tasks):
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

            tasks.append(Task(operator_id, question, solution, occurs_num, correct_num))

        return tasks

    def generate_foreign_language_tasks(self):
        tasks_id = nprand.choice(range(len(self.language_tasks)), size=self.number_of_tasks, replace=False)

        tasks = list()
        for id in tasks_id:
            tasks.append(Task(*self.language_tasks[id]))

        return tasks