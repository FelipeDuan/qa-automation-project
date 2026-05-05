class TestPet:
    def test_add_pet_returns_200(self, pet_service, pet_payload):
        response = pet_service.add_pet(pet_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == pet_payload["name"]
        assert data["status"] == "available"

    def test_add_pet_response_time(self, pet_service, pet_payload):
        response = pet_service.add_pet(pet_payload)
        assert response.elapsed.total_seconds() < 2

    def test_get_pet_by_id(self, pet_service, pet_payload):
        pet_service.add_pet(pet_payload)
        response = pet_service.get_pet(pet_payload["id"])
        assert response.status_code == 200
        assert response.json()["id"] == pet_payload["id"]

    def test_update_pet_status(self, pet_service, pet_payload):
        pet_service.add_pet(pet_payload)
        pet_payload["status"] = "sold"
        response = pet_service.update_pet(pet_payload)
        assert response.status_code == 200
        assert response.json()["status"] == "sold"

    def test_delete_pet(self, pet_service, pet_payload):
        pet_service.add_pet(pet_payload)
        response = pet_service.delete_pet(pet_payload["id"])
        assert response.status_code == 200

    def test_find_pets_by_status_available(self, pet_service):
        response = pet_service.find_by_status("available")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
