import pytest


@pytest.mark.user
@pytest.mark.smoke
class TestUserCRUD:
    def test_create_user(self, user_service, user_payload):
        response = user_service.create_user(user_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or "code" in data

    def test_get_user_by_username(self, user_service, user_payload):
        create_response = user_service.create_user(user_payload)
        assert create_response.status_code == 200
        
        response = user_service.get_user(user_payload["username"])
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == user_payload["username"]
        assert data["email"] == user_payload["email"]
        assert data["firstName"] == user_payload["firstName"]

    def test_update_user(self, user_service, user_payload):
        user_service.create_user(user_payload)
        
        user_payload["firstName"] = "UpdatedName"
        user_payload["email"] = f"updated_{user_payload['id']}@email.com"
        response = user_service.update_user(user_payload["username"], user_payload)
        
        assert response.status_code == 200

    def test_delete_user(self, user_service, user_payload):
        user_service.create_user(user_payload)
        
        response = user_service.delete_user(user_payload["username"])
        assert response.status_code == 200


@pytest.mark.user
class TestUserLogin:
    def test_user_login_success(self, user_service, user_payload):
        user_service.create_user(user_payload)
        
        response = user_service.login(user_payload["username"], user_payload["password"])
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data

    def test_user_login_response_time(self, user_service, user_payload):
        user_service.create_user(user_payload)
        
        response = user_service.login(user_payload["username"], user_payload["password"])
        assert response.elapsed.total_seconds() < 2


@pytest.mark.user
@pytest.mark.negative
class TestUserNegative:
    def test_get_nonexistent_user(self, user_service):
        response = user_service.get_user("nonexistent_user_999999")
        assert response.status_code == 404

    def test_create_user_without_username(self, user_service):
        invalid_payload = {
            "id": 123456,
            "firstName": "Test",
            "email": "test@test.com"
        }
        response = user_service.create_user(invalid_payload)
        assert response.status_code in [200, 400, 500]

    def test_delete_nonexistent_user(self, user_service):
        response = user_service.delete_user("nonexistent_user_999999")
        assert response.status_code == 404

    def test_login_with_wrong_password(self, user_service, user_payload):
        user_service.create_user(user_payload)
        
        response = user_service.login(user_payload["username"], "wrong_password")
        assert response.status_code in [200, 400]
