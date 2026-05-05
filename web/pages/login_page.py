from web.pages.base_page import BasePage
from web.locators.locators import LoginLocators


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type_text(LoginLocators.USERNAME, username)
        self.type_text(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(LoginLocators.ERROR_MESSAGE)
