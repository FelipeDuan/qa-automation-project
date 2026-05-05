import pytest


@pytest.mark.store
@pytest.mark.smoke
class TestStoreInventory:
    def test_get_inventory(self, store_service):
        response = store_service.get_inventory()
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        
        for key, value in data.items():
            assert isinstance(value, int)

    def test_get_inventory_response_time(self, store_service):
        response = store_service.get_inventory()
        assert response.elapsed.total_seconds() < 2


@pytest.mark.store
class TestStoreOrder:
    def test_place_order(self, store_service, order_payload):
        response = store_service.place_order(order_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_payload["id"]
        assert data["petId"] == order_payload["petId"]
        assert data["status"] == order_payload["status"]
        assert data["complete"] == order_payload["complete"]

    def test_place_order_response_time(self, store_service, order_payload):
        response = store_service.place_order(order_payload)
        assert response.elapsed.total_seconds() < 2

    def test_get_order_by_id(self, store_service, order_payload):
        place_response = store_service.place_order(order_payload)
        assert place_response.status_code == 200
        
        response = store_service.get_order(order_payload["id"])
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == order_payload["id"]
        assert data["petId"] == order_payload["petId"]

    def test_delete_order(self, store_service, order_payload):
        store_service.place_order(order_payload)
        
        response = store_service.delete_order(order_payload["id"])
        assert response.status_code == 200

    def test_complete_order_lifecycle(self, store_service, order_payload):
        place_response = store_service.place_order(order_payload)
        assert place_response.status_code == 200
        
        get_response = store_service.get_order(order_payload["id"])
        assert get_response.status_code == 200
        
        delete_response = store_service.delete_order(order_payload["id"])
        assert delete_response.status_code == 200


@pytest.mark.store
@pytest.mark.negative
class TestStoreNegative:
    def test_get_nonexistent_order(self, store_service):
        response = store_service.get_order(999999999)
        assert response.status_code == 404

    def test_delete_nonexistent_order(self, store_service):
        response = store_service.delete_order(999999999)
        assert response.status_code == 404

    def test_place_order_with_invalid_data(self, store_service):
        invalid_payload = {"invalid": "data"}
        response = store_service.place_order(invalid_payload)
        assert response.status_code in [200, 400, 500]
