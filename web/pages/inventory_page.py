from web.pages.base_page import BasePage
from web.locators.locators import InventoryLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class InventoryPage(BasePage):
    def is_loaded(self):
        return self.is_visible(InventoryLocators.INVENTORY_CONTAINER)

    def add_first_item_to_cart(self):
        print("[INVENTORY] Adding first item to cart...")
        time.sleep(0.5)
        
        self.wait.until(EC.presence_of_all_elements_located(InventoryLocators.ADD_TO_CART_BUTTONS))
        buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
        
        if buttons:
            button = buttons[0]
            self.scroll_to_element(button)
            time.sleep(0.5)
            
            print("[INVENTORY] Clicking 'Add to Cart' button...")
            try:
                button.click()
                print("[INVENTORY] Regular click succeeded")
            except Exception as e:
                print(f"[INVENTORY] Regular click failed: {e}, using JavaScript")
                self.driver.execute_script("arguments[0].click();", button)
            
            time.sleep(1.0)
            print("[INVENTORY] Waiting for cart badge to appear...")
            
            try:
                self.wait.until(EC.visibility_of_element_located(InventoryLocators.CART_BADGE))
                print("[INVENTORY] ✅ Cart badge appeared!")
            except Exception as e:
                print(f"[INVENTORY] ❌ Cart badge did NOT appear after 30s: {e}")
                raise

    def add_multiple_items_to_cart(self, count=2):
        print(f"[INVENTORY] Adding {count} items to cart...")
        time.sleep(0.5)
        
        for i in range(count):
            self.wait.until(EC.presence_of_all_elements_located(InventoryLocators.ADD_TO_CART_BUTTONS))
            buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
            
            if i >= len(buttons):
                print(f"[INVENTORY] Only {len(buttons)} items available, stopping at {i}")
                break
            
            button = buttons[i]
            self.scroll_to_element(button)
            time.sleep(0.5)
            
            print(f"[INVENTORY] Clicking item {i + 1}/{count}...")
            try:
                button.click()
                print(f"[INVENTORY] Item {i + 1} click succeeded")
            except Exception as e:
                print(f"[INVENTORY] Regular click failed: {e}, using JavaScript")
                self.driver.execute_script("arguments[0].click();", button)
            
            time.sleep(1.0)
            expected_count = str(i + 1)
            print(f"[INVENTORY] Waiting for badge to show '{expected_count}'...")
            
            try:
                self.wait.until(lambda d: self.get_cart_badge_text() == expected_count)
                print(f"[INVENTORY] ✅ Badge now shows {expected_count}")
            except Exception as e:
                current = self.get_cart_badge_text()
                print(f"[INVENTORY] ❌ Badge shows '{current}', expected '{expected_count}': {e}")
                raise

    def get_cart_badge_text(self):
        try:
            badge = self.driver.find_element(*InventoryLocators.CART_BADGE)
            return badge.text
        except:
            return "0"

    def get_cart_count(self):
        self.wait.until(EC.visibility_of_element_located(InventoryLocators.CART_BADGE))
        time.sleep(0.3)
        return self.get_text(InventoryLocators.CART_BADGE)

    def go_to_cart(self):
        print("[INVENTORY] Navigating to cart...")
        time.sleep(0.5)
        self.click(InventoryLocators.CART_LINK)
        time.sleep(1.0)
        print("[INVENTORY] ✅ Clicked cart link")
