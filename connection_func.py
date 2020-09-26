import json


class ConnectToJSON:
    def open_json(self, data_file):
        with open(data_file) as json_file:
            return json.load(json_file)
