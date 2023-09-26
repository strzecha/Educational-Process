from process import Process
from app import App
from data_reader import get_properties

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