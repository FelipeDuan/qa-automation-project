from web.pages.base_page import BasePage
from web.locators.locators import CartLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class CartPage(BasePage):
    def proceed_to_checkout(self):
        print("[CART] Proceeding to checkout...")
        time.sleep(0.5)
        
        try:
            self.wait.until(EC.visibility_of_element_located(CartLocators.CHECKOUT_BUTTON))
            print("[CART] Checkout button is visible")
        except Exception as e:
            print(f"[CART] ❌ Checkout button NOT visible: {e}")
            raise
        
        self.click(CartLocators.CHECKOUT_BUTTON)
        print("[CART] ✅ Clicked checkout button")
        time.sleep(1.0)

    def get_cart_items_count(self):
        print("[CART] Getting cart items count...")
        time.sleep(0.5)
        
        try:
            self.wait.until(EC.presence_of_all_elements_located(CartLocators.CART_ITEMS))
            items = self.driver.find_elements(*CartLocators.CART_ITEMS)
            count = len(items)
            print(f"[CART] Found {count} item(s)")
            return count
        except Exception as e:
            print(f"[CART] ❌ Could not find cart items: {e}")
            raise

    def remove_item(self):
        print("[CART] Removing item...")
        initial_count = self.get_cart_items_count()
        
        self.click(CartLocators.REMOVE_BUTTON)
        time.sleep(1.0)
        
        print(f"[CART] Waiting for count to change from {initial_count} to {initial_count - 1}...")
        self.wait_for_element_count(CartLocators.CART_ITEMS, initial_count - 1)
        print("[CART] ✅ Item removed")
        
    def is_cart_empty(self):
        print("[CART] Checking if cart is empty...")
        time.sleep(0.5)
        items = self.driver.find_elements(*CartLocators.CART_ITEMS)
        is_empty = len(items) == 0
        print(f"[CART] Cart empty: {is_empty}")
        return is_empty
