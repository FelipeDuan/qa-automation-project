import pytest


@pytest.mark.pet
@pytest.mark.smoke
class TestPetCRUD:
    def test_add_pet_returns_200(self, pet_service, pet_payload):
        response = pet_service.add_pet(pet_payload)
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        
        data = response.json()
        assert data["id"] == pet_payload["id"]
        assert data["name"] == pet_payload["name"]
        assert data["status"] == pet_payload["status"]
        assert "photoUrls" in data
        assert isinstance(data["photoUrls"], list)

    def test_add_pet_response_time(self, pet_service, pet_payload):
        response = pet_service.add_pet(pet_payload)
        assert response.elapsed.total_seconds() < 2

    def test_get_pet_by_id(self, pet_service, pet_payload):
        add_response = pet_service.add_pet(pet_payload)
        assert add_response.status_code == 200
        
        response = pet_service.get_pet(pet_payload["id"])
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == pet_payload["id"]
        assert data["name"] == pet_payload["name"]

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


@pytest.mark.pet
class TestPetSearch:
    def test_find_pets_by_status_available(self, pet_service):
        response = pet_service.find_by_status("available")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        if len(data) > 0:
            for pet in data[:5]:
                assert "status" in pet
                assert "id" in pet
                assert "name" in pet

    def test_find_pets_by_status_sold(self, pet_service):
        response = pet_service.find_by_status("sold")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_find_pets_by_status_pending(self, pet_service):
        response = pet_service.find_by_status("pending")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.pet
@pytest.mark.negative
class TestPetNegative:
    def test_get_nonexistent_pet(self, pet_service):
        response = pet_service.get_pet(999999999)
        assert response.status_code == 404

    def test_add_pet_without_required_fields(self, pet_service):
        invalid_payload = {"name": "NoPetId"}
        response = pet_service.add_pet(invalid_payload)
        assert response.status_code in [200, 400, 500]

    def test_delete_nonexistent_pet(self, pet_service):
        response = pet_service.delete_pet(999999999)
        assert response.status_code == 404
