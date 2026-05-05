from web.pages.base_page import BasePage
from web.locators.locators import LoginLocators
from api.utils.config import WEB_BASE_URL
import time


class LoginPage(BasePage):
    def open(self):
        print(f"[LOGIN] Opening {WEB_BASE_URL}")
        self.driver.get(WEB_BASE_URL)
        time.sleep(0.5)
        print("[LOGIN] ✅ Page opened")

    def login(self, username, password):
        print(f"[LOGIN] Logging in as '{username}'...")
        self.type_text(LoginLocators.USERNAME, username)
        self.type_text(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BUTTON)
        
        time.sleep(2.0)
        print("[LOGIN] Checking for password warning popup...")
        dismissed = self.dismiss_password_warning_popup()
        if dismissed:
            print("[LOGIN] ✅ Password warning popup was dismissed")
        else:
            print("[LOGIN] ✅ No popup (or already handled)")
        time.sleep(1.0)
        print("[LOGIN] ✅ Login completed")

    def get_error_message(self):
        print("[LOGIN] Getting error message...")
        error = self.get_text(LoginLocators.ERROR_MESSAGE)
        print(f"[LOGIN] Error: '{error}'")
        return error
    
    def is_error_displayed(self):
        print("[LOGIN] Checking if error is displayed...")
        is_displayed = self.is_visible(LoginLocators.ERROR_MESSAGE)
        print(f"[LOGIN] Error displayed: {is_displayed}")
        return is_displayed
