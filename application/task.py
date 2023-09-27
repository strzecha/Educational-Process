class Task:
    def __init__(self, id, question, solution, occurs_num, correct_num):
        self.id = id
        self.question = question
        self.solution = solution
        self.answer = ""
        self.occurs_num = occurs_num
        self.correct_num = correct_num

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
