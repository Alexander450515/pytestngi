from connection_func import ConnectToJSON
import pytest
import requests
import json

api = "/v2/entities"
url = "http://172.26.66.74:1026"
# with open('data.json') as f:
#     templates = json.load(f)


def test_create_entity_and_get_code_204():
    t1 = ConnectToJSON()
    t1.connect('data.json')
    response = requests.post(f"{url}{api}", json=t1.connect('data.json'))
    assert response.status_code == 201 or 204


# @pytest.mark.parametrize("api, expected_place_name", test_data_zip_codes)
def test_get_list_entities_and_code_200():
    response = requests.get(f"{url}{api}")
    assert response.status_code == 200






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