from web.pages.base_page import BasePage
from web.locators.locators import CartLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class CartPage(BasePage):
    def proceed_to_checkout(self):
        self.click(CartLocators.CHECKOUT_BUTTON)

    def get_cart_items_count(self):
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        return len(items)

    def remove_item(self):
        self.click(CartLocators.REMOVE_BUTTON)
        time.sleep(0.5)
        
    def is_cart_empty(self):
        time.sleep(0.3)
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        return len(items) == 0
