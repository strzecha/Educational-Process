from jproperties import Properties

def get_properties(file_name="properties"):
    configs = Properties()
    with open(file_name, 'rb') as config_file:
        configs.load(config_file, encoding="utf-8")

    return configs