from web.pages.base_page import BasePage
from web.locators.locators import CheckoutLocators
import time


class CheckoutPage(BasePage):
    FINISH_WAIT = 1.0
    
    def fill_info(self, first_name, last_name, postal_code):
        self.type_text(CheckoutLocators.FIRST_NAME, first_name)
        self.type_text(CheckoutLocators.LAST_NAME, last_name)
        self.type_text(CheckoutLocators.POSTAL_CODE, postal_code)
        self.click(CheckoutLocators.CONTINUE_BUTTON)

    def finish_purchase(self):
        self.click(CheckoutLocators.FINISH_BUTTON)
        time.sleep(self.FINISH_WAIT)

    def get_confirmation_message(self):
        return self.get_text(CheckoutLocators.COMPLETE_HEADER)
    
    def get_error_message(self):
        return self.get_text(CheckoutLocators.ERROR_MESSAGE)
