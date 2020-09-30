from connection_func import open_json
import pytest
import requests
import json

api = "/v2/entities"

templates_to_try = [
    # "templates", "templates_for_replace", "templates_for_append"
    ('json_files/entity_room.json', 'json_files/entity_room_replace.json',
     'json_files/entity_room_update_or_append.json'),
    # ('json_files/entity_room_1.json',)
]


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append"), templates_to_try)
def test_create_entity(url, templates, templates_for_replace, templates_for_append):
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


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append"), templates_to_try)
def test_replace_all_entity_attributes(url, templates, templates_for_replace, templates_for_append):
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


@pytest.mark.parametrize(("templates", "templates_for_replace", "templates_for_append"), templates_to_try)
def test_update_or_append_entity_attributes(url, templates, templates_for_replace, templates_for_append):
    templates = open_json(templates)
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    # Update or Append Entity Attributes
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


# def test_delete_entity():
#     json_file = ConnectToJSON()
#     templates = json_file.connect('entity_room.json')
#     response = requests.delete(f"{url}{api}/{templates['id']}")
#     assert response.status_code == 204
#     response = requests.get(f"{url}{api}/{templates['id']}/attrs")
#     assert response.status_code == 404


# def test_get_check_content_type_equals_json():
#     response = requests.get(url + api)
#     assert response.headers['Content-Type'] == "application/json"
#
#
# def test_get_entities_url_equals_entities():
#     response = requests.get(url + api)
#     response_body = response.json()
#     assert response_body["entities_url"] == "/v2/entities"
#
#
# def test_get_types_url_equals_types():
#     response = requests.get(url + api)
#     response_body = response.json()
#     assert response_body["types_url"] == "/v2/types"
#
#
# def test_get_subscriptions_url_equals_subscriptions():
#     response = requests.get(url + api)
#     response_body = response.json()
#     assert response_body["subscriptions_url"] == "/v2/subscriptions"
#
#
# def test_get_registrations_url_equals_registrations():
#     response = requests.get(url + api)
#     response_body = response.json()
#     assert response_body["registrations_url"] == "/v2/registrations"
