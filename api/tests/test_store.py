class TestStore:
    def test_get_inventory(self, store_service):
        response = store_service.get_inventory()
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_place_order(self, store_service, order_payload):
        response = store_service.place_order(order_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "placed"

    def test_place_order_response_time(self, store_service, order_payload):
        response = store_service.place_order(order_payload)
        assert response.elapsed.total_seconds() < 2

    def test_get_order_by_id(self, store_service, order_payload):
        store_service.place_order(order_payload)
        response = store_service.get_order(order_payload["id"])
        assert response.status_code == 200
        assert response.json()["id"] == order_payload["id"]

    def test_delete_order(self, store_service, order_payload):
        store_service.place_order(order_payload)
        response = store_service.delete_order(order_payload["id"])
        assert response.status_code == 200
