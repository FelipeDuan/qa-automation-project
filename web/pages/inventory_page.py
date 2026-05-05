from web.pages.base_page import BasePage
from web.locators.locators import InventoryLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class InventoryPage(BasePage):
    def is_loaded(self):
        return self.is_visible(InventoryLocators.INVENTORY_CONTAINER)

    def add_first_item_to_cart(self):
        self.wait.until(EC.presence_of_all_elements_located(InventoryLocators.ADD_TO_CART_BUTTONS))
        buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
        
        if buttons:
            button = buttons[0]
            self.scroll_to_element(button)
            time.sleep(0.3)
            
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click();", button)
            
            time.sleep(0.5)
            self.wait.until(EC.visibility_of_element_located(InventoryLocators.CART_BADGE))

    def add_multiple_items_to_cart(self, count=2):
        self.wait.until(EC.presence_of_all_elements_located(InventoryLocators.ADD_TO_CART_BUTTONS))
        buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
        
        for i in range(min(count, len(buttons))):
            button = buttons[i]
            self.scroll_to_element(button)
            time.sleep(0.2)
            
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click();", button)
            
            time.sleep(0.5)
            expected_count = str(i + 1)
            self.wait.until(lambda d: self.get_cart_badge_text() == expected_count)

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
        time.sleep(0.5)
        self.click(InventoryLocators.CART_LINK)
        time.sleep(0.5)
