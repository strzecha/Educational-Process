class Task:
    def __init__(self, id, question, solution, occurs_num, correct_num):
        self.id = id
        self.question = question
        self.solution = solution
        self.answer = ""
        self.occurs_num = occurs_num
        self.correct_num = correct_num
        self.probability = 0

    def get_occurs_num(self):
        return self.occurs_num
    
    def get_correct_num(self):
        return self.correct_num

    def get_probability(self):
        return self.probability

    def set_probability(self, prob):
        self.probability = prob

    def check(self, solution):
        return str(self.solution) == solution

    def get_solution(self):
        return self.solution

    def solve(self):
        self.answer = self.solution

    def __repr__(self):
        return f"{self.id} {self.correct_num}/{self.occurs_num}"
    
    def __str__(self):
        return "{} = {}".format(self.question, self.answer)

class MathTask(Task):
    def __init__(self, id, operator, occurs_num, correct_num):
        super().__init__(id, None, None, occurs_num, correct_num)
        self.operator = operator

    def set_question(self, question):
        self.question = question

    def set_solution(self, solution):
        self.solution = solution