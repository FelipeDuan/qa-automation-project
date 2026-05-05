class TestUser:
    def test_create_user(self, user_service, user_payload):
        response = user_service.create_user(user_payload)
        assert response.status_code == 200

    def test_get_user_by_username(self, user_service, user_payload):
        user_service.create_user(user_payload)
        response = user_service.get_user(user_payload["username"])
        assert response.status_code == 200
        assert response.json()["username"] == user_payload["username"]

    def test_user_login(self, user_service, user_payload):
        user_service.create_user(user_payload)
        response = user_service.login(user_payload["username"], user_payload["password"])
        assert response.status_code == 200

    def test_update_user(self, user_service, user_payload):
        user_service.create_user(user_payload)
        user_payload["firstName"] = "Updated"
        response = user_service.update_user(user_payload["username"], user_payload)
        assert response.status_code == 200

    def test_delete_user(self, user_service, user_payload):
        user_service.create_user(user_payload)
        response = user_service.delete_user(user_payload["username"])
        assert response.status_code == 200
