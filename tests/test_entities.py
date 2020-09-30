from connection_func import open_json
import pytest
import requests
import json

api = "/v2/entities"

templates_to_try = [
    # ("templates", "templates_for_replace", "templates_for_append")
    ('json_files/entity_room.json', 'json_files/entity_room_replace.json',
     'json_files/entity_room_update_or_append.json', "entity_room_update"),
    ('json_files/entity_room_1.json', 'json_files/entity_room_replace_1.json',
     'json_files/entity_room_update_or_append_1.json', "entity_room_update_1"),
]


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append", "templates_for_update"),
                         templates_to_try)
def test_create_entity(url, templates, templates_for_replace, templates_for_append, templates_for_update):
    # Создание
    templates = open_json(templates)
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    response = requests.get(f"{url}{api}/{templates['id']}")
    assert response.status_code == 200
    response_body = response.json()
    for key in templates:
        if key in ('id', 'type'):
            assert response_body[key] == templates[key]
        else:
            assert response_body[key]['value'] == templates[key]['value']
    # Проверка корректности создания /v2/entities/{entityId}/attrs
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 200
    response_body = response.json()
    for key in templates:
        if key in ('id', 'type'):
            continue
        assert response_body[key]['value'] == templates[key]['value']
    # Удаление
    response = requests.delete(f"{url}{api}/{templates['id']}")
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 404


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append", "templates_for_update"),
                         templates_to_try)
def test_replace_all_entity_attributes(url, templates, templates_for_replace, templates_for_append,
                                       templates_for_update):
    # Создание
    templates = open_json(templates)
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    templates_for_replace = open_json(templates_for_replace)
    response = requests.put(f"{url}{api}/{templates['id']}/attrs", json=templates_for_replace)
    assert response.status_code == 204
    # Проверка замены атрибутов
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    response_body = response.json()
    for key in templates_for_replace:
        assert response_body[key]['value'] == templates_for_replace[key]['value']
    # Удаление
    response = requests.delete(f"{url}{api}/{templates['id']}")
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 404


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append", "templates_for_update"),
                         templates_to_try)
def test_update_or_append_entity_attributes(url, templates, templates_for_replace, templates_for_append,
                                            templates_for_update):
    # Создание
    templates = open_json(templates)
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    # Добавление и замена
    templates_for_append = open_json(templates_for_append)
    response = requests.post(f"{url}{api}/{templates['id']}/attrs", json=templates_for_append)
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    response_body = response.json()
    for key in templates_for_append:
        assert response_body[key]['value'] == templates_for_append[key]['value']
    # Удаление
    response = requests.delete(f"{url}{api}/{templates['id']}")
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 404


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append", "templates_for_update"),
                         templates_to_try)
def test_update_existing_entity_attributes(url, templates, templates_for_replace, templates_for_append,
                                           templates_for_update):
    # Создание
    templates = open_json(templates)
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    # Добавление и замена
    templates_for_append = open_json(templates_for_update)
    response = requests.patch(f"{url}{api}/{templates['id']}/attrs", json=templates_for_update)
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    response_body = response.json()
    for key in templates_for_append:
        assert response_body[key]['value'] == templates_for_append[key]['value']
    # Удаление
    response = requests.delete(f"{url}{api}/{templates['id']}")
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 404
