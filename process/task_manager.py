import random

from process.task import Task

OPERATORS = ["+", "-", "*", "/"]
NUM_TASKS = 10

class TaskManager:
    def generate_tasks(self):
        tasks = list()

        for _ in range(NUM_TASKS):
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

            tasks.append(Task(num1, num2, operator))

        return tasks