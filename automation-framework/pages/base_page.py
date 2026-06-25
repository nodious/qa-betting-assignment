"""Base Page Object for System"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import settings


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, path: str = ""):
        url = f"{settings.BASE_URL}{path}?user-id={settings.USER_ID}"
        self.driver.get(url)

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or settings.DEFAULT_TIMEOUT)

    def find(self, locator):
        return self._wait().until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self._wait().until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(str(text))

    def get_text(self, locator):
        return self.find(locator).text

    def get_attribute(self, locator, attribute):
        return self.find(locator).get_attribute(attribute)

    def is_visible(self, locator, timeout=None):
        """Return True if the element becomes visible within the timeout, else False"""
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_until_gone(self, locator, timeout=None):
        """Wait until an element is no longer present/visible"""
        return self._wait(timeout).until(EC.invisibility_of_element_located(locator))