from api.client.base_client import BaseClient
from api.utils.config import BASE_URL


class StoreService(BaseClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def place_order(self, order_data):
        return self.post("/store/order", json=order_data)

    def get_order(self, order_id):
        return self.get(f"/store/order/{order_id}")

    def delete_order(self, order_id):
        return self.delete(f"/store/order/{order_id}")

    def get_inventory(self):
        return self.get("/store/inventory")
