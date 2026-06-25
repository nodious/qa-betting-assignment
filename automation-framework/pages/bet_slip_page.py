"""Page Object for the Bet Slip"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BetSlipPage(BasePage):
    """ Bet Slip Static Locators """

    bet_slip_locator = (By.XPATH, "//*[@id='bet-slip']")
    teams_locator = (By.XPATH, "//*[@id='bet-slip']//div[contains(@class,'Teams')]")
    match_winner_locator = (By.XPATH, "//*[@id='bet-slip']//div[contains(@class,'betSelectionMarket')]")
    odds_locator = (By.XPATH, "//*[@id='bet-slip']//span[contains(@class,'Odds')]")
    stake_input_locator = (By.XPATH, "//input[@id='bet-slip-stake-input']")
    total_stake_locator = (By.XPATH, "//span[@id='bet-slip-total-stake']")
    potential_payout_locator = (By.XPATH, "//span[@id='bet-slip-potential-payout']")

    place_bet_button_locator = (By.XPATH, "//button[@id='bet-slip-place-bet']")
    placing_indicator_locator = (By.XPATH, "//button[contains(@class,'Placing')]")

    """ Bet Slip Methods """

    def is_bet_slip_visible(self):
        return self.is_visible(self.bet_slip_locator)

    def get_teams_names(self):
        """Return (home_name, away_name) parsed from the bet slip teams text."""
        teams_text = self.get_text(self.teams_locator)
        teams_lines = teams_text.splitlines()
        if len(teams_lines) >= 3:
            home_name = teams_lines[0].strip()
            away_name = teams_lines[2].strip()
            return home_name, away_name
        raise ValueError("Unexpected format for teams text in bet slip.")

    def get_match_winner(self):
        """Return the selected outcome ('home' / 'draw' / 'away'), lowercased."""
        match_winner_text = self.get_text(self.match_winner_locator)
        match_winner_lines = match_winner_text.splitlines()
        if len(match_winner_lines) >= 2:
            return match_winner_lines[1].strip().lower()
        raise ValueError("Unexpected format for match winner text in bet slip.")

    def get_odds_value(self):
        """Return the odds shown in the slip as a float (e.g. 'Odds: 2.50' -> 2.5)."""
        odds_text = self.get_text(self.odds_locator)
        return float(odds_text.replace("Odds:", "").strip())

    def enter_stake(self, amount):
        """Enter the stake amount in the input field (1.00 to 100.00 euros)."""
        self.type_text(self.stake_input_locator, amount)

    def get_total_stake(self):
        """Return the total stake shown in the slip as a float (e.g. '€12.00' -> 12.0)."""
        total_stake_text = self.get_text(self.total_stake_locator)
        return float(total_stake_text.replace("€", "").strip())

    def get_potential_payout(self):
        """Return the potential payout shown in the slip as a float (e.g. '€29.42' -> 29.42)."""
        potential_payout_text = self.get_text(self.potential_payout_locator)
        return float(potential_payout_text.replace("€", "").strip())

    def place_bet(self):
        """Click Place Bet. Resolution (receipt appearing) is awaited by the test via ReceiptModal."""
        self.click(self.place_bet_button_locator)

    def is_placing_indicator_visible(self):
        """Return True if the 'Placing...' indicator is visible, else False."""
        return self.is_visible(self.placing_indicator_locator)

    def wait_until_placing_indicator_gone(self, timeout=None):
        """Wait until the 'Placing...' indicator is no longer present/visible."""
        return self.wait_until_gone(self.placing_indicator_locator, timeout)