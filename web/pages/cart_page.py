from web.pages.base_page import BasePage
from web.locators.locators import CartLocators


class CartPage(BasePage):
    def proceed_to_checkout(self):
        self.click(CartLocators.CHECKOUT_BUTTON)

    def get_cart_items_count(self):
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        return len(items)

    def remove_item(self):
        self.click(CartLocators.REMOVE_BUTTON)
        
    def is_cart_empty(self):
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        return len(items) == 0
