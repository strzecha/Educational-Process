from ast import operator
from asyncio import tasks
import pygame
import random

from process.task import Task
from process.button import Button
from process.text import Text

class Process:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.BGCOLOG = (200, 200, 200)
        
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.font_size = int(0.05 * self.screen_height)

        text = Text("Sprawdź", (0, 0, 0), pos_x = 400, pos_y=105, font_size=self.font_size)

        self.check_button = Button(0.2 * self.screen_width, 0.075 * self.screen_height, 0.4 * self.screen_width, 0.9 * self.screen_height, text, 
                                    self.stop, color=(150, 150, 150), hover_color=(100, 100, 100))

    def prepare_tasks(self):
        tasks = list()

        for i in range(10):
            num2 = random.randint(1, 10)
            operator = random.choice(["+", "-", "*", "/"])

            if operator == "/":
                num1 = num2 * random.randint(1, 10)
            else:
                num1 = random.randint(1, 10)

            tasks.append(Task(num1, num2, operator))

        self.tasks = tasks
        self.tasks_gui = list()

        i = 0
        for task in tasks:
            pos_x = 0.2 * self.screen_width + (i // 5) * 0.4 * self.screen_width
            pos_y = 0.2 * self.screen_height + ((i % 5)) * 0.12 * self.screen_height
            self.tasks_gui.append(Text(str(task), (0, 0, 0), pos_x=pos_x, pos_y=pos_y, font_size=self.font_size))
            i += 1

    def stop(self):
        self.run = False

    def update(self):
        self.check_button.update()
        pygame.display.update()

    def draw(self):
        self.check_button.draw(self.window)
        for task in self.tasks_gui:
            task.draw(self.window)


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

                self.check_button.handle_event(event)

            self.window.fill(self.BGCOLOG)
            self.draw()
            self.update()

        pygame.quit()