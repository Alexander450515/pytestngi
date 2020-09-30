import json


def open_json(data_file):
    with open(data_file) as json_file:
        return json.load(json_file)

