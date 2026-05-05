from web.pages.base_page import BasePage
from web.locators.locators import LoginLocators
from api.utils.config import WEB_BASE_URL


class LoginPage(BasePage):
    def open(self):
        self.driver.get(WEB_BASE_URL)

    def login(self, username, password):
        self.type_text(LoginLocators.USERNAME, username)
        self.type_text(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(LoginLocators.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        return self.is_visible(LoginLocators.ERROR_MESSAGE)
