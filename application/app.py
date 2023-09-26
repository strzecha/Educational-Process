import pygame
import os

from application.task import Task
from application.task_manager import TaskManager
from gui.button import Button
from gui.text import Text
from gui.text_input import InputText
from utils.database import update_language_task, update_math_task, create_connection

class App:
    def __init__(self):
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

    def prepare_tasks(self):
        manager = TaskManager()
        self.tasks = manager.generate_tasks()
        self.num = manager.get_num()

        self.tasks_gui = list()
        self.solution_gui = list()

        if self.num == 0:
            i = 0
            for task in self.tasks:
                pos_x = 0.15 * self.screen_width + (i // 5) * 0.35 * self.screen_width
                pos_y = 0.2 * self.screen_height + ((i % 5)) * 0.12 * self.screen_height
                self.tasks_gui.append(Text(str(task), (0, 0, 0), pos_x=pos_x, pos_y=pos_y, font_size=self.font_size))
                self.solution_gui.append(InputText(0.10 * self.screen_width, 0.05 * self.screen_height, pos_x=pos_x+0.20*self.screen_width, pos_y=pos_y, font_size=self.font_size))
                i += 1

        elif self.num == 1:
            i = 0
            for task in self.tasks:
                pos_x = 0.2 * self.screen_width
                pos_y = 0.1 * self.screen_height + i * 0.08 * self.screen_height
                self.tasks_gui.append(Text(str(task), (0, 0, 0), pos_x=pos_x, pos_y=pos_y, font_size=self.font_size))
                self.solution_gui.append(InputText(0.2 * self.screen_width, 0.05 * self.screen_height, pos_x=pos_x+0.4*self.screen_width, pos_y=pos_y, font_size=self.font_size))
                i += 1

    def stop(self):
        self.run = False

    def update(self):
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
        points = 0
        connection = create_connection() 
        for i in range(len(self.tasks)):
            answer = self.solution_gui[i].get_text()
            correct = 0
            if self.tasks[i].check(answer):
                points += 1
                correct = 1
                self.solution_gui[i].set_background_color((22, 255, 18))
            else:
                self.solution_gui[i].set_background_color((252, 18, 18))

            if self.num == 0: # math tasks
                update_math_task(connection, self.tasks[i].id, correct)
            if self.num == 1: # language tasks
                update_language_task(connection, self.tasks[i].id, correct)

            self.tasks[i].solve()
            self.tasks_gui[i].set_text(str(self.tasks[i])) 
        connection.close()
        if points < 9:
            self.restart_state = True
        else:
            self.ended = True
            text = Text("Wyjdź", (0, 0, 0), font_size=self.font_size)
            self.next_button.set_text(text)

        self.update()

    def restart(self):
        if self.ended:
            self.run = False
        elif self.restart_state:
            self.prepare_tasks()
            self.restart_state = False    

    def draw(self):
        if self.restart_state or self.ended:
            self.next_button.draw(self.window)
        else:
            self.check_button.draw(self.window)
        for task in self.tasks_gui:
            task.draw(self.window)
        for solution in self.solution_gui:
            solution.draw(self.window)


    def start(self):
        self.run = True

        self.prepare_tasks()
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