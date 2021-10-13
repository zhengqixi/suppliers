from app import app
import json

test_app = app.test_client()


def test_create_happy_path():
    response = test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test',
                                'email': 'nice'
                            }), content_type='application/json')
    assert response is not None
    assert response.status_code == 200
    assert response.is_json
    assert 'id' in response.json


def test_create_no_contact():
    response = test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test',
                            }), content_type='application/json')
    assert response is not None
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json


def test_create_incorrect_data_type():
    response = test_app.put('/supplier',
                            data=json.dumps({
                                'name': 177013,
                            }), content_type='application/json')
    assert response is not None
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json
