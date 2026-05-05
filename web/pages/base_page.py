from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
    
    def dismiss_password_warning_popup(self):
        """
        Método mantido por compatibilidade, mas não é mais necessário.
        
        O popup de "vazamento de senha" foi resolvido através de flags do Chrome
        em driver_factory.py:
        - --disable-password-manager-reauthentication
        - --disable-save-password-bubble
        - profile.password_manager_leak_detection: False
        
        Este método apenas retorna False pois o popup não aparece mais.
        """
        return False

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.scroll_to_element(element)
        
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        
        time.sleep(0.3)

    def click_with_retry(self, locator, retries=3):
        for attempt in range(retries):
            try:
                self.click(locator)
                return True
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(0.5)
        return False

    def type_text(self, locator, text):
        element = self.find_element(locator)
        self.scroll_to_element(element)
        element.clear()
        time.sleep(0.1)
        element.send_keys(text)
        time.sleep(0.2)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False
    
    def wait_for_element_count(self, locator, expected_count, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            elements = self.driver.find_elements(*locator)
            if len(elements) == expected_count:
                return True
            time.sleep(0.3)
        return False
