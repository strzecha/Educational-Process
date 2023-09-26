from application.process import Process
from application.app import App
from utils.data_reader import get_properties

properties = get_properties()

DEBUG = properties.get("DEBUG").data

def main():
    if DEBUG == "FALSE":
        proc = Process()
        proc.start()
    else:
        app = App()
        app.start()

if __name__ == "__main__":
    main()