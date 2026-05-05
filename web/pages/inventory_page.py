from web.pages.base_page import BasePage
from web.locators.locators import InventoryLocators


class InventoryPage(BasePage):
    def is_loaded(self):
        return self.find_element(InventoryLocators.INVENTORY_CONTAINER) is not None

    def add_first_item_to_cart(self):
        buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
        buttons[0].click()

    def get_cart_count(self):
        return self.get_text(InventoryLocators.CART_BADGE)

    def go_to_cart(self):
        self.click(InventoryLocators.CART_LINK)
