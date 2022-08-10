import os
import json
import pytest
from unittest import mock
from test.util import read_file
from test.unit.mock_app import MockApp


@pytest.fixture(autouse=True)
def props():
    with mock.patch.dict(os.environ, 
        {'JWT_PUBLIC_KEY': read_file('public.key')}):
        yield


def test_401_missing_header():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API)
    assert 401 == response.status_code
    assert 'Success' != _get_response_body(response)


def test_401_malformed_header_value():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': 'malformed'})
    assert 401 == response.status_code
    assert 'Success' != _get_response_body(response)


def test_401_scheme_only():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': 'Bearer'})
    assert 401 == response.status_code
    assert MockApp.RESPONSE != _get_response_body(response)


def test_401_invalid_scheme():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': f"Invalid {read_file('access_token_valid.txt')}"})
    assert 401 == response.status_code
    assert MockApp.RESPONSE != _get_response_body(response)


def test_401_refresh_token():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': f"Bearer {read_file('refresh_token_valid.txt')}"})
    assert 401 == response.status_code
    assert MockApp.RESPONSE != _get_response_body(response)


def test_401_expired_token():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': f"Bearer {read_file('access_token_expired.txt')}"})
    assert 401 == response.status_code
    assert MockApp.RESPONSE != _get_response_body(response)


def test_401_invalid_signature():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': f"Bearer {read_file('access_token_bad_signature.txt')}"})
    assert 401 == response.status_code
    assert MockApp.RESPONSE != _get_response_body(response)


def test_200():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get(MockApp.PRIVATE_API, headers={'Authorization': f"Bearer {read_file('access_token_valid.txt')}"})
    assert 200 == response.status_code
    assert MockApp.RESPONSE == _get_response_body(response)


def _get_response_body(response):
    return json.loads(response.get_data(as_text=True))
