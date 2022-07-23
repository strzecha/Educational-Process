from ast import operator
import pygame
import random

from process.task import Task
from process.button import Button
from process.text import Text

class Process:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        text = Text("Sprawdź", (0, 0, 0), pos_x = 400, pos_y=105)

        self.check_button = Button(200, 30, 400, 800, text, self.stop)

    def prepare_tasks(self):
        tasks = list()

        for i in range(10):
            num2 = random.randint(0, 10)
            operator = random.choice(["+", "-", "*", "/"])

            if operator == "/":
                num1 = num2 * random.randint(0, 10)
            else:
                num1 = random.randint(0, 10)

            tasks.append(Task(num1, num2, operator))

        return tasks

    def stop(self):
        self.run = False

    def update(self):
        self.check_button.update()
        pygame.display.update()

    def draw(self):
        self.check_button.draw(self.window)


    def start(self):
        self.run = True

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()

                self.check_button.handle_event(event)

            self.window.fill((0, 0, 0))
            self.draw()
            self.update()

        pygame.quit()