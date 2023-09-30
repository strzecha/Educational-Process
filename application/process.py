import time

from application.app import App
from utils.data_reader import get_properties

properties = get_properties()

DELAY = int(properties.get("DELAY").data)

class Process:
    """class Process

    Class to representation of process which runs an application
    """

    def start(self):
        """Main method of Process
        """

        while True:
            app = App()
            app.start()
            time.sleep(DELAY)