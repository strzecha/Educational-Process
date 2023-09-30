import random
import numpy.random as nprand
from copy import deepcopy

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

MATH_TASKS = 0
LANGUAGE_TASKS = 1

class TaskManager:
    """class TaskManager

    Class to generate and manage tasks in application
    """

    def __init__(self):
        """Init method
        """

        self.add_range = ADD_RANGE
        self.sub_range = SUB_RANGE
        self.mul_range = MUL_RANGE
        self.div_range = DIV_RANGE

        self.language_tasks = None
        self.number_of_tasks = NUM_TASKS

        self.tasks_type = None

    def get_tasks_and_set_probability(self):
        """Method to get tasks from database and set theirs probabilities of occurs
        """

        db = TaskDatabase()
        if db.connection:
            self.math_tasks = db.get_all_math_tasks()
            self.language_tasks = db.get_all_language_tasks()

            db.close()

        occurs_total = 0

        for task in (self.math_tasks + self.language_tasks):
            prob = task.get_probability()
            prob += (task.get_occurs_num() - task.get_correct_num())
            task.set_probability(prob)

            occurs_total += task.get_occurs_num()

        prob_total = 0

        for task in (self.math_tasks + self.language_tasks):
            prob = task.get_probability()
            prob += (occurs_total - task.get_occurs_num())
            task.set_probability(prob)

            prob_total += prob

        for task in (self.math_tasks + self.language_tasks):
            prob = task.get_probability()
            prob /= prob_total
            task.set_probability(prob)

    def generate_tasks(self):
        """Method to randomly generate tasks

        Returns:
            list: chosen tasks
        """
        
        self.get_tasks_and_set_probability()
        
        tasks = list()
        self.tasks_type = random.randint(0, 1)

        if self.tasks_type == MATH_TASKS:
            tasks = self.generate_math_tasks()
        elif self.tasks_type == LANGUAGE_TASKS:
            tasks = self.generate_foreign_language_tasks()

        return tasks

    def get_tasks_type(self):
        """Getter tasks type

        Returns:
            int: type of tasks
        """
        return self.tasks_type

    def generate_math_tasks(self):
        """Method to randomly generate math tasks

        Returns:
            list: chosen tasks
        """

        probs = [task.get_probability() for task in self.math_tasks]
        probabilities = [p / sum(probs) for p in probs]
        tasks_templates = nprand.choice(self.math_tasks, size=self.number_of_tasks, replace=True, p=probabilities)
        tasks = list()
        for task_template in tasks_templates:
            if task_template.operator == "+":
                num1 = random.randint(*self.add_range)
                num2 = random.randint(*self.add_range)
            elif task_template.operator == "-":
                num1 = random.randint(*self.sub_range)
                num2 = random.randint(self.sub_range[0], num1)
            elif task_template.operator == "*":
                num1 = random.randint(*self.mul_range)
                num2 = random.randint(*self.mul_range)
            elif task_template.operator == "/":
                num2 = random.randint(*self.div_range)
                num2 = max(num2, 1)
                num1 = random.randint(*self.div_range) * num2
            
            question = f"{num1} {task_template.operator} {num2}"
            solution = int(eval(question))

            task = deepcopy(task_template)
            task.set_question(question)
            task.set_solution(solution)
            tasks.append(task)

        return tasks

    def generate_foreign_language_tasks(self):
        """Method to randomly generate language tasks

        Returns:
            list: chosen tasks
        """

        probs = [task.get_probability() for task in self.language_tasks]
        probabilities = [p / sum(probs) for p in probs]
        tasks = nprand.choice(self.language_tasks, size=self.number_of_tasks, replace=False, p=probabilities)
        return tasks