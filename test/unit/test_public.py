import json
from test.unit.mock_app import MockApp


def test_public():
    app = MockApp().run()
    client = app.test_client({'TESTING': True})
    response = client.get('/public')
    assert 200 == response.status_code
    assert MockApp.RESPONSE == json.loads(response.get_data(as_text=True))
