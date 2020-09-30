import json

with open('tests/json_files/entity_room.json') as f:
    templates = json.load(f)

with open('tests/json_files/entity_room.json') as f:
    templates_1 = json.load(f)

print(templates == templates_1)


