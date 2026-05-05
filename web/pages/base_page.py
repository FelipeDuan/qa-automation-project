from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Classe base com ações reutilizáveis. Todas as pages herdam daqui."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        """Aguarda elemento ficar visível antes de retorná-lo."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Aguarda elemento ser clicável antes de clicar."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text
