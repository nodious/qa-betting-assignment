"""Page Object for the Bet Slip"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BetSlipPage(BasePage):
    """ Bet Slip Static Locators """

    bet_slip_locator = (By.XPATH, "//*[@id='bet-slip']")
    teams_locator = (By.XPATH, "//*[@id='bet-slip']//div[contains(@class,'betSelectionTeams')]")
    match_winner_locator = (By.XPATH, "//*[@id='bet-slip']//div[contains(@class,'betSelectionMarket')]")
    odds_locator = (By.XPATH, "//*[@id='bet-slip']//span[contains(@class,'betSelectionOdds')]")
    stake_input_locator = (By.XPATH, "//input[@id='bet-slip-stake-input']")
    total_stake_locator = (By.XPATH, "//span[@id='bet-slip-total-stake']")
    potential_payout_locator = (By.XPATH, "//span[@id='bet-slip-potential-payout']")

    place_bet_button_locator = (By.XPATH, "//button[@id='bet-slip-place-bet']")
    placing_indicator_locator = (By.XPATH, "//button[contains(@class,'Placing')]")

    """ Bet Slip Methods """

    def is_bet_slip_visible(self):
        return self.is_visible(self.bet_slip_locator)

    def get_teams_names(self):
        """Return (home, away) from the single-line 'Home vs Away' selection text"""
        teams_text = self.get_text(self.teams_locator)
        parts = teams_text.split(" vs ")
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        raise ValueError(f"Unexpected teams format in bet slip: {teams_text!r}")

    def get_match_winner(self):
        """Return the selected outcome ('home' / 'draw' / 'away') from 'Match Winner: Home'"""
        market_text = self.get_text(self.match_winner_locator)
        return market_text.split(":")[-1].strip().lower()

    def get_odds_value(self):
        """Return the odds as a float"""
        odds_text = self.get_text(self.odds_locator)
        return float(odds_text.split(":")[-1].strip())

    def enter_stake(self, amount):
        """Enter the stake amount in the input field (1.00 to 100.00 euros)"""
        self.type_text(self.stake_input_locator, amount)

    def get_total_stake(self):
        """Return the total stake as a float"""
        total_stake_text = self.get_text(self.total_stake_locator)
        return float(total_stake_text.split("€")[-1].replace(",", "").strip())

    def get_potential_payout(self):
        """Return the potential payout as a float"""
        payout_text = self.get_text(self.potential_payout_locator)
        return float(payout_text.split("€")[-1].replace(",", "").strip())

    def place_bet(self):
        self.click(self.place_bet_button_locator)

    def is_placing_indicator_visible(self):
        return self.is_visible(self.placing_indicator_locator)

    def wait_until_placing_indicator_gone(self, timeout=None):
        return self.wait_until_gone(self.placing_indicator_locator, timeout)