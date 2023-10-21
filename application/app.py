import pygame
import os
import datetime

from application.task_manager import TaskManager, MATH_TASKS, LANGUAGE_TASKS
from gui.button import Button
from gui.text import Text
from gui.text_input import InputText
from utils.database import TaskDatabase, create_database
from utils.data_reader import get_properties, check_properties
from utils.mail_sender import MailSender

properties = get_properties()

DB_FILE = properties.get("TASKS_DB_NAME").data
WEEK_DB_FILE = properties.get("TASKS_WEEK_DB_NAME").data
LANGUAGE_TASKS_TABLE_NAME = properties.get("LANGUAGE_TASKS_TABLE_NAME").data
MATH_TASKS_TABLE_NAME = properties.get("MATH_TASKS_TABLE_NAME").data
THRESHOLD = int(properties.get("THRESHOLD").data)

class App:
    """class App

    Class to representation of main processes in programme
    """

    def __init__(self):
        """Init method
        """

        check_properties()

        pygame.init()

        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.BGCOLOG = (200, 200, 200)
        
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.font_size = int(0.05 * self.screen_height)

        text = Text("Sprawdź", (0, 0, 0), font_size=self.font_size)

        self.check_button = Button(0.2 * self.screen_width, 0.075 * self.screen_height, 0.5 * self.screen_width, 0.9 * self.screen_height, text, 
                                    self.check_answers, color=(150, 150, 150), hover_color=(100, 100, 100))

        text = Text("Restart", (0, 0, 0), font_size=self.font_size)

        self.next_button = Button(0.2 * self.screen_width, 0.075 * self.screen_height, 0.3 * self.screen_width, 0.9 * self.screen_height, text, 
                                    self.restart, color=(150, 150, 150), hover_color=(100, 100, 100))

        self.restart_state = False
        self.ended = False
        self.main_db = TaskDatabase(DB_FILE)
        self.weekly_db = TaskDatabase(WEEK_DB_FILE) 
        self.threshold = THRESHOLD

        self.tasks_type = None

    def prepare_tasks_to_display(self):
        """Method to prepare tasks to display on screen
        """

        manager = TaskManager()
        self.tasks = manager.generate_tasks(self.tasks_type)
        self.tasks_type = manager.get_tasks_type()

        self.tasks_gui = list()
        self.solution_gui = list()

        if self.tasks_type == MATH_TASKS:
            i = 0
            for task in self.tasks:
                pos_x = 0.15 * self.screen_width + (i // 5) * 0.35 * self.screen_width
                pos_y = 0.2 * self.screen_height + ((i % 5)) * 0.12 * self.screen_height
                self.tasks_gui.append(Text(str(task), (0, 0, 0), pos_x=pos_x, pos_y=pos_y, font_size=self.font_size))
                self.solution_gui.append(InputText(0.10 * self.screen_width, 0.05 * self.screen_height, pos_x=pos_x + 0.20 * self.screen_width,
                                                    pos_y=pos_y, font_size=self.font_size))
                i += 1

        elif self.tasks_type == LANGUAGE_TASKS:
            i = 0
            for task in self.tasks:
                pos_x = 0.2 * self.screen_width
                pos_y = 0.1 * self.screen_height + i * 0.08 * self.screen_height
                self.tasks_gui.append(Text(str(task), (0, 0, 0), pos_x=pos_x, pos_y=pos_y, font_size=self.font_size))
                self.solution_gui.append(InputText(0.2 * self.screen_width, 0.05 * self.screen_height, pos_x=pos_x + 0.4 * self.screen_width, 
                                                   pos_y=pos_y, font_size=self.font_size))
                i += 1

    def stop(self):
        """Method to stop application
        """

        self.run = False

    def update(self):
        """Method to update display
        """

        if self.restart_state or self.ended:
            self.next_button.update()
        else:
            self.check_button.update()
        for solution in self.solution_gui:
            solution.update()
        for task in self.tasks_gui:
            task.update()
        pygame.display.update()

    def check_answers(self):
        """Method to check answers to tasks
        """

        points = 0
        for i in range(len(self.tasks)):
            answer = self.solution_gui[i].get_text()
            correct = 0
            if self.tasks[i].check(answer):
                points += 1
                correct = 1
                self.solution_gui[i].set_background_color((22, 255, 18))
            else:
                self.solution_gui[i].set_background_color((252, 18, 18))

            if self.tasks_type == MATH_TASKS:
                self.main_db.update_math_task(self.tasks[i].id, correct)
                self.weekly_db.update_math_task(self.tasks[i].id, correct)
            if self.tasks_type == LANGUAGE_TASKS:
                self.main_db.update_language_task(self.tasks[i].id, correct)
                self.weekly_db.update_language_task(self.tasks[i].id, correct)

            self.tasks[i].solve()
            self.tasks_gui[i].set_text(str(self.tasks[i])) 
        if points < self.threshold:
            self.restart_state = True
        else:
            self.ended = True
            text = Text("Wyjdź", (0, 0, 0), font_size=self.font_size)
            self.next_button.set_text(text)

        self.update()

    def restart(self):
        """Method to restart application
        """

        if self.ended:
            self.stop()
        elif self.restart_state:
            self.prepare_tasks_to_display()
            self.restart_state = False    

    def draw(self):
        """Method to draw elements of application
        """

        if self.restart_state or self.ended:
            self.next_button.draw(self.window)
        else:
            self.check_button.draw(self.window)
        for task in self.tasks_gui:
            task.draw(self.window)
        for solution in self.solution_gui:
            solution.draw(self.window)

    def start(self):
        """Main method of App
        """

        self.run = True

        current_date = datetime.datetime.now()
        current_week = current_date.isocalendar().week

        if os.path.exists("sent"):
            file = open("sent", "r+")
            num_of_week = int(file.readline())

            if num_of_week != current_week:
                self.send_email()
                self.weekly_db.close()
                os.remove(WEEK_DB_FILE)
                create_database(WEEK_DB_FILE)
                self.weekly_db = TaskDatabase(WEEK_DB_FILE)
                file.seek(0)
                file.write(str(current_week))
                file.truncate()
        else:
            file = open("sent", "w")
            file.write(str(current_week))

        self.prepare_tasks_to_display()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()
                    if event.key == pygame.K_LSUPER or event.key == pygame.K_RSUPER:
                        os.system("shutdown /s /t 1")

                if self.restart_state or self.ended:
                    self.next_button.handle_event(event)
                else:
                    self.check_button.handle_event(event)
                    for solution in self.solution_gui:
                        solution.handle_event(event)
                

            self.window.fill(self.BGCOLOG)
            self.draw()
            self.update()

        pygame.quit()
        self.main_db.close()
        self.weekly_db.close()

    def calculate_accuracy(self, db):   
        """Method to calculate accuracy of user on tasks from database

        Args:
            db (TaskDatabase): database with tasks

        Returns:
            int: total occurs of math tasks
            int: total correct answers to math tasks
            float: accuracy of user on math tasks
            int: total occurs of language tasks
            int: total correct answers to language tasks
            float: accuracy of user on language tasks
        """     

        math_occurs_total = db.count_total_occurs(MATH_TASKS_TABLE_NAME)
        math_correct_total = db.count_total_correct(MATH_TASKS_TABLE_NAME)

        language_occurs_total = db.count_total_occurs(LANGUAGE_TASKS_TABLE_NAME)
        language_correct_total = db.count_total_correct(LANGUAGE_TASKS_TABLE_NAME)

        math_accuracy_total = round(math_correct_total / math_occurs_total, 4) if math_occurs_total > 0 else 0
        language_accuracy_total = round(language_correct_total / language_occurs_total, 4) if language_correct_total > 0 else 0
    
        return (math_occurs_total, math_correct_total, math_accuracy_total, 
                language_occurs_total, language_correct_total, language_accuracy_total)
    
    def calculate_total_accuracy(self):
        """Method to calculate total accuracy of user on tasks
        """
        (
            self.math_occurs_total, self.math_correct_total, self.math_accuracy_total, 
            self.language_occurs_total, self.language_correct_total, self.language_accuracy_total
        ) = self.calculate_accuracy(self.main_db)
        (
            self.math_occurs_week, self.math_correct_week, self.math_accuracy_week, 
            self.language_occurs_week, self.language_correct_week, self.language_accuracy_week
        ) = self.calculate_accuracy(self.weekly_db)
    
    def send_email(self):
        """Method to send an email with report
        """   
        
        self.calculate_total_accuracy()

        message = f"""
            Tygodniowe podsumowanie:
            Skuteczność w zadaniach z matematyki: {self.math_correct_week}/{self.math_occurs_week} ({self.math_accuracy_week * 100}%)
            Skuteczność w zadaniach z języka angielskiego: {self.language_correct_week}/{self.language_occurs_week} ({self.language_accuracy_week * 100}%)
            Całkowite podsumowanie:
            Skuteczność w zadaniach z matematyki: {self.math_correct_total}/{self.math_occurs_total} ({self.math_accuracy_total * 100}%)
            Skuteczność w zadaniach z języka angielskiego: {self.language_correct_total}/{self.language_occurs_total} ({self.language_accuracy_total * 100}%)
            """
        
        ms = MailSender()
        ms.create_mail(message)
        ms.send_mail()