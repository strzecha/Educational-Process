from tkinter import SOLID


class Task:
    def __init__(self, solution):
        self.solution = solution
        self.answer = ""

    def check(self, solution):
        return self.solution == solution

    def get_solution(self):
        return self.solution

    def solve(self):
        self.answer = self.solution

class MathTask(Task):
    def __init__(self, number1, number2, operator):
        super().__init__(int(eval(str(number1)+operator+str(number2))))
        self.number1 = number1
        self.number2 = number2
        self.operator = operator

    def __str__(self):
        return "{} {} {} = {}".format(self.number1, self.operator, self.number2, self.answer)

    def check(self, solution):
        try:
            solution = int(solution)
            return self.solution == solution
        except:
            return False

class ForeignLanguageTask(Task):
    def __init__(self, word, translation):
        super().__init__(translation)
        self.word = word

    def __str__(self):
        return "{} - {}".format(self.word, self.answer)