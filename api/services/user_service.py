from api.client.base_client import BaseClient
from api.utils.config import BASE_URL


class UserService(BaseClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def create_user(self, user_data):
        return self.post("/user", json=user_data)

    def get_user(self, username):
        return self.get(f"/user/{username}")

    def update_user(self, username, user_data):
        return self.put(f"/user/{username}", json=user_data)

    def delete_user(self, username):
        return self.delete(f"/user/{username}")

    def login(self, username, password):
        return self.get("/user/login", params={"username": username, "password": password})
