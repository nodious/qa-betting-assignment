"""Page Object for the Success Receipt modal shown after a bet is placed"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ReceiptModal(BasePage):
    """ Receipt Modal Static Locators """

    modal_title_locator = (By.XPATH, "//h2[contains(@class,'modalTitle')]")
    bet_id_locator = (By.XPATH, "//*[@id='modal-success-bet-id']")
    match_locator = (By.XPATH, "//*[@id='modal-success-match']")
    stake_locator = (By.XPATH, "//*[@id='modal-success-stake']")
    odds_locator = (By.XPATH, "//*[@id='modal-success-odds']")
    payout_locator = (By.XPATH, "//*[@id='modal-success-payout']")
    timestamp_locator = (By.XPATH, "//*[@id='modal-success-placed-at']")
    close_button_locator = (By.XPATH, "//*[@id='modal-success-close']")

    """ Receipt Modal Methods """

    def is_displayed(self, timeout=None):
        return self.is_visible(self.modal_title_locator, timeout)

    def get_bet_id(self):
        """Return the bet ID text shown on the receipt"""
        return self.get_text(self.bet_id_locator).strip()

    def get_match(self):
        """Return (home_name, away_name) from the single-line 'Home vs Away' match label"""
        match_text = self.get_text(self.match_locator)
        parts = match_text.split(" vs ")
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        raise ValueError(f"Unexpected match format in receipt: {match_text!r}")

    def get_odds_value(self):
        """Return the odds shown on the receipt as a float """
        return float(self.get_text(self.odds_locator).strip())

    def get_stake(self):
        """Return the stake shown on the receipt as a float """
        stake_text = self.get_text(self.stake_locator)
        return float(stake_text.split("€")[-1].replace(",", "").strip())

    def get_payout(self):
        """Return the potential payout shown on the receipt as a float """
        payout_text = self.get_text(self.payout_locator)
        return float(payout_text.split("€")[-1].replace(",", "").strip())

    def get_timestamp(self):
        """Return the placement timestamp text shown on the receipt"""
        return self.get_text(self.timestamp_locator).strip()

    def close(self):
        self.click(self.close_button_locator)