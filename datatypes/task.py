class Task:
    """Class Task

    Class to representation of task in application
    """

    def __init__(self, id, question, solution, occurs_num, correct_num):
        """Init method

        Args:
            id (int): id of tasks
            question (str): contents of task
            solution (str): solution of task
            occurs_num (int): number of occurs task in application
            correct_num (int): number of correct answert to task
        """

        self.id = id
        self.question = question
        self.solution = solution
        self.answer = ""
        self.occurs_num = occurs_num
        self.correct_num = correct_num
        self.probability = 0

    def get_occurs_num(self):
        """Getter of occurs_num

        Returns:
            int: number of occurs of task
        """

        return self.occurs_num
    
    def get_correct_num(self):
        """Getter of correct_num

        Returns:
            int: number of correct answers to task
        """

        return self.correct_num

    def get_probability(self):
        """Getter of probability

        Returns:
            float: probability of tasks's occurs
        """

        return self.probability

    def set_probability(self, prob):
        """Setter of probability

        Args:
            prob (float): probability of tasks's occurs
        """

        self.probability = prob

    def check(self, answer):
        """Method to check if answer is correct

        Args:
            answer (str): user's answer to task

        Returns:
            bool: if answer is correct
        """

        return str(self.solution) == answer

    def get_solution(self):
        """Getter of solution

        Returns:
            str: solution of task
        """

        return self.solution
    
    def set_question(self, question):
        """Setter of question
        
        Args:
            question (str): constents of task
        """

        self.question = question

    def set_solution(self, solution):
        """Setter of solution

        Args:
            solution (int): solution of task
        """
        self.solution = solution

    def solve(self):
        """Method to solve task
        """
        
        self.answer = self.solution

    def __repr__(self):
        """Representation method
        """
        
        return f"{self.id} {self.correct_num}/{self.occurs_num}"
    
    def __str__(self):
        """String method
        """
        
        return "{} = {}".format(self.question, self.answer)

class MathTask(Task):
    """Class MathTask
    
    Class to representation of math task
    """
    
    def __init__(self, id, operator, occurs_num, correct_num):
        """Init method

        Args:
            id (int): ID of task
            operator (str): operator of math task
            occurs_num (int): number of occurs task in application
            correct_num (int): number of correct answert to task
        """
        super().__init__(id, None, None, occurs_num, correct_num)
        self.operator = operator

    