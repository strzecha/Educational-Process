import time

from app import App

class Process:
    def start(self):
        while True:
            app = App()
            app.start()
            time.sleep(60)