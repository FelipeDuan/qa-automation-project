import pytest
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
def pet_payload():
    return {
        "id": 999991,
        "name": "TestDog",
        "status": "available",
        "photoUrls": ["http://example.com/photo.jpg"]
    }


@pytest.fixture
def user_payload():
    return {
        "id": 999991,
        "username": "testuser_qa_auto",
        "firstName": "Test",
        "lastName": "User",
        "email": "testqa@email.com",
        "password": "senha123",
        "phone": "11999999999",
        "userStatus": 1
    }


@pytest.fixture
def order_payload():
    return {
        "id": 999991,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }
