import time

from app import App
from data_reader import get_properties

properties = get_properties()

DELAY = int(properties.get("DELAY").data)

class Process:
    def start(self):
        while True:
            app = App()
            app.start()
            time.sleep(DELAY)