from api.client.base_client import BaseClient
from api.utils.config import BASE_URL


class PetService(BaseClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def add_pet(self, pet_data):
        return self.post("/pet", json=pet_data)

    def get_pet(self, pet_id):
        return self.get(f"/pet/{pet_id}")

    def update_pet(self, pet_data):
        return self.put("/pet", json=pet_data)

    def delete_pet(self, pet_id):
        return self.delete(f"/pet/{pet_id}")

    def find_by_status(self, status):
        return self.get("/pet/findByStatus", params={"status": status})
