import pytest
import random
from api.services.pet_service import PetService
from api.services.user_service import UserService
from api.services.store_service import StoreService


@pytest.fixture
def pet_service():
    return PetService()


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def store_service():
    return StoreService()


@pytest.fixture
def random_id():
    return random.randint(100000, 999999)


@pytest.fixture
def pet_payload(random_id):
    return {
        "id": random_id,
        "name": f"TestDog_{random_id}",
        "status": "available",
        "photoUrls": ["http://example.com/photo.jpg"],
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "tags": [
            {
                "id": 1,
                "name": "test"
            }
        ]
    }


@pytest.fixture
def user_payload(random_id):
    return {
        "id": random_id,
        "username": f"testuser_{random_id}",
        "firstName": "Test",
        "lastName": "User",
        "email": f"test_{random_id}@email.com",
        "password": "senha123",
        "phone": "11999999999",
        "userStatus": 1
    }


@pytest.fixture
def order_payload(random_id):
    return {
        "id": random_id,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }
