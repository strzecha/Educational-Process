import time

from process.app import App

class Process:
    def start(self):
        while True:
            time.sleep(60)

            app = App()

            app.start()