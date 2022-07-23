class Task:
    def __init__(self, number1, number2, operator):
        self.number1 = number1
        self.number2 = number2
        self.operator = operator
        self.solution = eval(str(number1)+operator+str(number2))