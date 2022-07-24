from numpy import number


class Task:
    def __init__(self, number1, number2, operator):
        self.number1 = number1
        self.number2 = number2
        self.operator = operator
        self.solution = int(eval(str(number1)+operator+str(number2)))

    def __str__(self):
        return "{} {} {} = ".format(self.number1, self.operator, self.number2)

    def check(self, solution):
        return self.solution == solution

    def get_solution(self):
        return self.solution