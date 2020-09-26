from connection_func import ConnectToJSON
import pytest
import requests
import json

api = "/v2/entities"
url = "http://172.26.66.74:1026"


def test_create_entity():
    json_file = ConnectToJSON()
    templates = json_file.connect('entity_room.json')
    # POST запрос /v2/entities
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    # Проверка корректности создания /v2/entities/{entityId}
    response = requests.get(f"{url}{api}/{templates['id']}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["type"] == templates["type"]
    assert response_body["id"] == templates["id"]
    assert response_body["temperature"]["value"] == templates["temperature"]["value"] and (
        (type(response_body["temperature"]["value"]) in (float, int)))
    assert response_body["humidity"]["value"] == templates["humidity"]["value"] and (
            (type(templates["humidity"]["value"])) in (float, int))
    assert response_body["location"]["value"] == templates["location"]["value"]
    assert response_body["location"]["type"] == templates["location"]["type"]
    assert response_body["location"]["metadata"]["crs"]["value"] == templates["location"]["metadata"]["crs"]["value"]
    # Проверка корректности создания /v2/entities/{entityId}/attrs
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["temperature"]["value"] == templates["temperature"]["value"] and (
        (type(response_body["temperature"]["value"]) in (float, int)))
    assert response_body["humidity"]["value"] == templates["humidity"]["value"] and (
            (type(templates["humidity"]["value"])) in (float, int))
    assert response_body["location"]["value"] == templates["location"]["value"]
    assert response_body["location"]["type"] == templates["location"]["type"]
    assert response_body["location"]["metadata"]["crs"]["value"] == templates["location"]["metadata"]["crs"]["value"]
    response = requests.delete(f"{url}{api}/{templates['id']}")
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 404


def test_replace_all_entity_attributes():
    json_file = ConnectToJSON()
    templates = json_file.connect('entity_room.json')
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    json_file_for_replace = ConnectToJSON()
    templates_for_replace = json_file_for_replace.connect('entity_room_replace.json')
    response = requests.put(f"{url}{api}/{templates['id']}/attrs", json=templates_for_replace)
    assert response.status_code == 204
    # Проверка замены атрибутов
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    response_body = response.json()
    assert response_body["temperature"]["value"] == templates_for_replace["temperature"]["value"] and (
        (type(response_body["temperature"]["value"]) in (float, int)))
    assert response_body["seatNumber"]["value"] == templates_for_replace["seatNumber"]["value"] and (
        (type(response_body["seatNumber"]["value"]) in (float, int)))
    response = requests.delete(f"{url}{api}/{templates['id']}")
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    assert response.status_code == 404


def test_update_or_append_entity_attributes():
    json_file = ConnectToJSON()
    templates = json_file.connect('entity_room.json')
    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)
    json_file_for_append = ConnectToJSON()
    templates_for_append = json_file_for_append.connect('entity_room_append.json')
    # POST запрос /v2/entities/{entityId}/attrs
    # Update or Append Entity Attributes
    response = requests.post(f"{url}{api}/{templates['id']}/attrs", json=templates_for_append)
    assert response.status_code == 204
    response = requests.get(f"{url}{api}/{templates['id']}/attrs")
    response_body = response.json()
    assert response_body["ambientNoise"]["value"] == templates_for_append["ambientNoise"]["value"] and (
        (type(response_body["ambientNoise"]["value"]) in (float, int)))
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
