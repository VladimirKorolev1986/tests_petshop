import requests
import pytest

BASE_URL = 'https://petstore.swagger.io/v2'


@pytest.fixture(scope='module')
def create_order():
    order_data = {
        "id": 9876,
        "petId": 123,
        "quantity": 1,
        "shipDate": "2023-10-01T00:00:00Z",
        "status": "placed",
        "complete": False
    }
    response = requests.post(f'{BASE_URL}/store/order', json=order_data)
    assert response.status_code == 200
    return response.json()


def test_place_order(create_order):
    assert create_order['petId'] == 123
    assert create_order['status'] == 'placed'


def test_get_inventory():
    response = requests.get(f'{BASE_URL}/store/inventory')
    assert response.status_code == 200
    inventory = response.json()
    assert isinstance(inventory, dict)


def test_find_order_by_id(create_order):
    response = requests.get(f'{BASE_URL}/store/order/{create_order["id"]}')
    assert response.status_code == 200
    order = response.json()
    assert order['id'] == create_order['id']


def test_delete_order(create_order):
    response = requests.delete(f'{BASE_URL}/store/order/{create_order["id"]}')
    assert response.status_code == 200
    response = requests.get(f'{BASE_URL}/store/order/{create_order["id"]}')
    assert response.status_code == 404
