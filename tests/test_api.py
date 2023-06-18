import requests
import re
from schemas.reqres import user_schema, delay_schema
from pytest_voluptuous import S


def test_get_single_user_status_200():
    url = 'https://reqres.in/api/users/2'
    response = requests.get(url)
    assert response.status_code == 200


def test_get_single_user_content_type():
    url = 'https://reqres.in/api/users/2'
    response = requests.get(url)
    assert response.headers["content-type"] == 'application/json; charset=utf-8'


def test_get_single_user_schema():
    url = 'https://reqres.in/api/users/2'
    response = requests.get(url)
    assert S(user_schema) == response.json()


def test_get_delayed_response_status_200():
    url = 'https://reqres.in/api/users'
    response = requests.get(url, params={"delay": 3})
    assert response.status_code == 200


def test_get_delayed_response_per_page():
    url = 'https://reqres.in/api/users'
    response = requests.get(url, params={"delay": 3})
    assert response.json()["per_page"] == 6


def test_get_delayed_response_scheme():
    url = 'https://reqres.in/api/users'
    response = requests.get(url, params={"delay": 3})
    assert S(delay_schema) == response.json()


def test_post_login_successful_token_len():
    url = 'https://reqres.in/api/login'
    response = requests.post(url, {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })
    assert len(response.json()["token"]) == 17


def test_post_login_unsuccessful_status_400():
    url = 'https://reqres.in/api/login'
    response = requests.post(url, data={"email": "peter@klaven"})
    assert response.status_code == 400


def test_patch_update_time():
    url = 'https://reqres.in/api/users/2'
    response = requests.patch(url, data={
        "name": "morpheus",
        "job": "zion resident"
    })
    assert re.search(r"\d{4}\D\d{2}\D\d{2}", response.json()["updatedAt"])


def test_delete_status_204():
    url = 'https://reqres.in/api/users/2'
    response = requests.delete(url)
    assert response.status_code == 204
