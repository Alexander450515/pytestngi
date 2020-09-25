from connection_func import ConnectToJSON
import pytest
import requests
import json

api = "/v2/entities"
url = "http://172.26.66.74:1026"


def test_create_entity():
    json_file = ConnectToJSON()
    templates = json_file.connect('data.json')

    response = requests.post(f"{url}{api}", json=templates)
    assert response.status_code in (201, 204)

    response = requests.get(f"{url}{api}?id={templates['id']}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["type"] == templates["type"]
    assert response_body[0]["id"] == templates["id"]
    assert response_body[0]["temperature"]["value"] == templates["temperature"]["value"] and (
        (type(response_body[0]["temperature"]["value"]) in (float, int)))
    assert response_body[0]["humidity"]["value"] == templates["humidity"]["value"] and (
            (type(templates["humidity"]["value"])) in (float, int))
    assert response_body[0]["location"]["value"] == templates["location"]["value"]
    assert response_body[0]["location"]["type"] == templates["location"]["type"]
    assert response_body[0]["location"]["metadata"]["crs"]["value"] == templates["location"]["metadata"]["crs"]["value"]

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
