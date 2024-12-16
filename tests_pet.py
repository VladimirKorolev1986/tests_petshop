import requests
import pytest

BASE_URL = 'https://petstore.swagger.io/v2'


@pytest.fixture(scope='module')
def new_pet():
    data = {
        "id": 123,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(f'{BASE_URL}/pet', json=data)
    assert response.status_code == 200
    return response.json()


def test_create_pet(new_pet):
    assert new_pet['name'] == 'Buddy'
    assert new_pet['status'] == 'available'


def test_update_pet(new_pet):
    updated_data = {"name": "Max"}
    response = requests.put(f'{BASE_URL}/pet/{new_pet["id"]}', json=updated_data)
    assert response.status_code == 200
    updated_pet = response.json()
    assert updated_pet['name'] == 'Max'


def test_get_pet_by_id(new_pet):
    response = requests.get(f'{BASE_URL}/pet/{new_pet["id"]}')
    assert response.status_code == 200
    pet = response.json()
    assert pet['id'] == new_pet['id']


def test_delete_pet(new_pet):
    response = requests.delete(f'{BASE_URL}/pet/{new_pet["id"]}')
    assert response.status_code == 200
    response = requests.get(f'{BASE_URL}/pet/{new_pet["id"]}')
    assert response.status_code == 404
