import json


class ConnectToJSON:
    def connect(self, data_file):
        with open(data_file) as json_file:
            return json.load(json_file)

    # def get_data(self, name):
    #     for student in self.__data["students"]:
    #         if student["name"] == name:
    #             return student
