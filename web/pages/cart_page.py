from web.pages.base_page import BasePage
from web.locators.locators import CartLocators
from selenium.webdriver.support import expected_conditions as EC
import time


class CartPage(BasePage):
    CHECKOUT_WAIT = 1.0
    
    def proceed_to_checkout(self):
        self.wait.until(EC.visibility_of_element_located(CartLocators.CHECKOUT_BUTTON))
        self.click(CartLocators.CHECKOUT_BUTTON)
        time.sleep(self.CHECKOUT_WAIT)

    def get_cart_items_count(self):
        self.wait.until(EC.presence_of_all_elements_located(CartLocators.CART_ITEMS))
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        return len(items)

    def remove_item(self):
        initial_count = self.get_cart_items_count()
        self.click(CartLocators.REMOVE_BUTTON)
        time.sleep(self.CHECKOUT_WAIT)
        self.wait_for_element_count(CartLocators.CART_ITEMS, initial_count - 1)
        
    def is_cart_empty(self):
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        return len(items) == 0
