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
    assert response.status_code == 201
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

    
def test_read_correct():
    test_app.put('/supplier',
        data=json.dumps({
            'name': 'Tom',
            'email': 'Tom@gmail.com',
            'address': 'New York',
            'products': [1, 2, 3]
            }), content_type='application/json')
    response = test_app.get('/supplier/1')
    assert response is not None
    assert response.is_json
    assert response.status_code == 200

def test_read_correct_data():
    test_app.put('/supplier',
        data=json.dumps({
            'name': 'Tom',
            'email': 'Tom@gmail.com',
            'address': 'New York',
            'products': [1, 2, 3]
            }), content_type='application/json')
    response = test_app.get('/supplier/1')
    assert response is not None
    assert response.is_json
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == 1

def test_read_not_found():
    response = test_app.get('/supplier/10000')
    assert response is not None
    assert response.is_json
    assert response.status_code == 404
    assert 'error' in response.json

def test_read_correct():
    test_app.put('/supplier',
        data=json.dumps({
            'name': 'Tom',
            'email': 'Tom@gmail.com',
            'address': 'New York',
            'products': [1, 2, 3]
            }), content_type='application/json')
    response = test_app.get('/supplier/1')
    assert response is not None
    assert response.is_json
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == 1

def test_update_not_found():
    response = test_app.post('/supplier/10000')
    assert response is not None
    assert response.is_json
    assert response.status_code == 404
    assert 'error' in response.json

def test_update_and_read_correct():
    test_app.put('/supplier',
        data=json.dumps({
            'name': 'Tom',
            'email': 'Tom@gmail.com',
            'address': 'New York',
            'products': [1, 2, 3]
            }), content_type='application/json')
    test_app.post('/supplier/1',
        data=json.dumps({
            'name': 'update1',
            'email': 'update1@gmail.com',
            'address': 'NYU',
            'products': [2]
            }), content_type='application/json')
    response = test_app.get('/supplier/1')
    assert response is not None
    assert response.is_json
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == 1
    assert response.json['name'] == 'update1'
    assert response.json['email'] == 'update1@gmail.com'
    assert response.json['address'] == 'NYU'
    assert response.json['products'] == [2]

def test_delete_non_empty_database():
    test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test1',
                                'email': 'email1',
                                'address': 'address1',
                                'products': [100, 200, 300]
                            }), content_type='application/json')

    test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test2',
                                'email': 'email2',
                                'address': 'address2',
                                'products': [400, 500, 600]
                            }), content_type='application/json')

    response1 = test_app.delete("/supplier/1")
    assert response1 is not None
    assert response1.status_code == 200
    assert 'id' in response1.json
    assert response1.json['id'] == 1
    
    response2 = test_app.delete("/supplier/2")
    assert response2 is not None
    assert response2.status_code == 200
    assert 'id' in response1.json
    assert response2.json['id'] == 2


def test_delete_not_found():
    test_app.put('/supplier',
                 data=json.dumps({
                     'name': 'test1',
                     'email': 'email1',
                     'address': 'address1',
                     'products': [100, 200, 300]
                 }), content_type='application/json')

    test_app.put('/supplier',
                 data=json.dumps({
                     'name': 'test2',
                     'email': 'email2',
                     'address': 'address2',
                     'products': [400, 500, 600]
                 }), content_type='application/json')

    response = test_app.delete("/supplier/100")
    assert response is not None
    assert response.is_json
    assert response.status_code == 400
    assert 'error' in response.json



def test_list_all_suppliers():
    test_app.put('/supplier',
                 data=json.dumps({
                     'name': 'test1',
                     'email': 'email1',
                     'address': 'address1',
                     'products': [100, 200, 300]
                 }), content_type='application/json')

    test_app.put('/supplier',
                 data=json.dumps({
                     'name': 'test2',
                     'email': 'email2',
                     'address': 'address2',
                     'products': [400, 500, 600]
                 }), content_type='application/json')

    test_app.put('/supplier',
                 data=json.dumps({
                     'name': 'test3',
                     'email': 'email3',
                     'address': 'address3',
                     'products': [700, 800, 900]
                 }), content_type='application/json')

    test_app.put('/supplier',
                 data=json.dumps({
                     'name': 'test4',
                     'email': 'email4',
                     'address': 'address4',
                     'products': [1000, 1100, 1200]
                 }), content_type='application/json')

    response = test_app.get('/suppliers')
    assert response is not None
    assert response.status_code == 200
    assert response.is_json
