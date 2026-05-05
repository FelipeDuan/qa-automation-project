from web.pages.base_page import BasePage
from web.locators.locators import InventoryLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage(BasePage):
    def is_loaded(self):
        return self.is_visible(InventoryLocators.INVENTORY_CONTAINER)

    def add_first_item_to_cart(self):
        self.wait.until(EC.presence_of_all_elements_located(InventoryLocators.ADD_TO_CART_BUTTONS))
        buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()

    def add_multiple_items_to_cart(self, count=2):
        self.wait.until(EC.presence_of_all_elements_located(InventoryLocators.ADD_TO_CART_BUTTONS))
        buttons = self.driver.find_elements(*InventoryLocators.ADD_TO_CART_BUTTONS)
        for i in range(min(count, len(buttons))):
            buttons[i].click()

    def get_cart_count(self):
        return self.get_text(InventoryLocators.CART_BADGE)

    def go_to_cart(self):
        self.click(InventoryLocators.CART_LINK)
