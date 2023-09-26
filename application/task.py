from tkinter import SOLID


class Task:
    def __init__(self, id, solution, occurs_num, correct_num):
        self.id = id
        self.solution = solution
        self.answer = ""
        self.occurs_num = occurs_num
        self.correct_num = correct_num

    def check(self, solution):
        return self.solution == solution

    def get_solution(self):
        return self.solution

    def solve(self):
        self.answer = self.solution

    def __repr__(self):
        return f"{self.id} {self.correct_num}/{self.occurs_num}"

class MathTask(Task):
    def __init__(self, id, number1, number2, operator, occurs_num, correct_num):
        super().__init__(id, int(eval(str(number1)+operator+str(number2))), occurs_num, correct_num)
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
    def __init__(self, id, word, translation, occurs_num, correct_num):
        super().__init__(id, translation, occurs_num, correct_num)
        self.word = word

    def __str__(self):
        return "{} - {}".format(self.word, self.answer)