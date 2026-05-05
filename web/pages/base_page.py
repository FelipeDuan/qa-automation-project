from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time


class BasePage:
    DEFAULT_TIMEOUT = 30
    SMALL_WAIT = 0.2
    MEDIUM_WAIT = 0.5
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(self.SMALL_WAIT)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.scroll_to_element(element)
        
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        
        time.sleep(self.SMALL_WAIT)

    def type_text(self, locator, text):
        element = self.find_element(locator)
        self.scroll_to_element(element)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_count(self, locator, expected_count, timeout=10):
        end_time = time.time() + timeout
        while time.time() < end_time:
            elements = self.driver.find_elements(*locator)
            if len(elements) == expected_count:
                return True
            time.sleep(self.SMALL_WAIT)
        return False
