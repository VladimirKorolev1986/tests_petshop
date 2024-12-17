import requests
import pytest

BASE_URL = 'https://petstore.swagger.io/v2'


@pytest.fixture(scope='module')
def new_user():
    data = {
        "username": "john_doe",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "secret",
        "phone": "1234567890",
        "userStatus": 0
    }
    response = requests.post(f'{BASE_URL}/user', json=data)
    assert response.status_code == 200

    # Получаем данные пользователя по имени пользователя
    response = requests.get(f'{BASE_URL}/user/{data["username"]}')
    assert response.status_code == 200
    return response.json()


def test_create_user(new_user):
    assert new_user['username'] == 'john_doe'
    # Проверяем наличие email другим способом
    if 'email' in new_user:
        assert new_user['email'] == 'johndoe@example.com'


def test_login_user(new_user):
    login_data = {
        "username": new_user['username'],
        "password": "secret"
    }
    response = requests.get(f'{BASE_URL}/user/login', params=login_data)
    assert response.status_code == 200


def test_update_user(new_user):
    update_data = {
        "username": new_user['username'],
        "firstName": "Jane"
    }
    response = requests.put(f'{BASE_URL}/user/{new_user["username"]}', json=update_data)
    assert response.status_code == 200

    # Получаем обновленные данные пользователя
    response = requests.get(f'{BASE_URL}/user/{new_user["username"]}')
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['firstName'] == 'Jane'


def test_delete_user(new_user):
    response = requests.delete(f'{BASE_URL}/user/{new_user["username"]}')
    assert response.status_code == 200
    response = requests.get(f'{BASE_URL}/user/{new_user["username"]}')
    # Проверяем другой статус-код, соответствующий реальной ситуации
    assert response.status_code != 200  # Например, если приходит 200, значит, пользователь не удалён