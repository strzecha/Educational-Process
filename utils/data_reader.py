import csv

from jproperties import Properties

def get_properties(file_name="properties"):
    configs = Properties()
    with open(file_name, 'rb') as config_file:
        configs.load(config_file, encoding="utf-8")

    return configs

def read_data_words_from_file(filename):
    results = list()
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', fieldnames=["word", "translation"])
        for row in reader:
            results.append(row)

    return results