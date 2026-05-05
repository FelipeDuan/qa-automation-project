from web.pages.base_page import BasePage
from web.locators.locators import CheckoutLocators
import time


class CheckoutPage(BasePage):
    def fill_info(self, first_name, last_name, postal_code):
        print(f"[CHECKOUT] Filling info: '{first_name}', '{last_name}', '{postal_code}'")
        time.sleep(0.3)
        
        self.type_text(CheckoutLocators.FIRST_NAME, first_name)
        self.type_text(CheckoutLocators.LAST_NAME, last_name)
        self.type_text(CheckoutLocators.POSTAL_CODE, postal_code)
        
        print("[CHECKOUT] Clicking continue button...")
        self.click(CheckoutLocators.CONTINUE_BUTTON)
        time.sleep(0.5)
        print("[CHECKOUT] ✅ Info filled and submitted")

    def finish_purchase(self):
        print("[CHECKOUT] Finishing purchase...")
        time.sleep(0.3)
        
        self.click(CheckoutLocators.FINISH_BUTTON)
        time.sleep(1.0)
        print("[CHECKOUT] ✅ Purchase finished")

    def get_confirmation_message(self):
        print("[CHECKOUT] Getting confirmation message...")
        message = self.get_text(CheckoutLocators.COMPLETE_HEADER)
        print(f"[CHECKOUT] Message: '{message}'")
        return message
    
    def get_error_message(self):
        print("[CHECKOUT] Getting error message...")
        error = self.get_text(CheckoutLocators.ERROR_MESSAGE)
        print(f"[CHECKOUT] Error: '{error}'")
        return error
