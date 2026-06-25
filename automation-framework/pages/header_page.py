"""Page Object for the top header bar — logo, profile, and the user's balance."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HeaderPage(BasePage):
    """ Header Static Locators """

    header_locator = (By.XPATH, "//*[@id='app-header']")
    header_brand_locator = (By.XPATH, "//*[@id='app-header']//div[contains(@id,'header-brand')]")
    balance_locator = (By.XPATH, "//*[@id='header-balance']//span[contains(.,'Balance')]")

    """ Header Methods """

    def is_header_visible(self):
        return self.is_visible(self.header_locator)

    def is_header_brand_visible(self):
        return self.is_visible(self.header_brand_locator)

    def get_balance(self):
        """Return the balance shown in the header as a float (e.g. 'Balance: €120.00' -> 120.0)."""
        balance_text = self.get_text(self.balance_locator)
        return self._parse_money(balance_text)

    def _parse_money(self, text):
        """Extract the euro amount from balance text and return a float"""
        amount = text.split("€")[-1]
        return float(amount.replace(",", "").strip())