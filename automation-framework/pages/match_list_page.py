"""Page Object for the match list — the matches and their odds buttons."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import random


class MatchListPage(BasePage):
    """ Match List Page Static Locators"""

    match_list_locator = (By.XPATH, "//*[@id='match-list']")
    match_list_all_cards_locator = (By.XPATH, "//*[@id='match-list']//div[contains(@class, 'matchCard')]")

    """ Match List Page Dynamic Locators"""

    def specific_match_card_locator(self, match_id):
        return (By.XPATH, f"//*[@id='match-card-{match_id}']")

    def specific_match_odds_button_locator(self, match_id, selection):
        """ selection:  'home', 'draw', 'away' """
        return (By.XPATH, f"//*[@id='match-card-{match_id}']//button[contains(@id, '{match_id}-{selection}')]")

    def specific_match_odds_value_locator(self, match_id, selection):
        """ selection:  'home', 'draw', 'away' """
        return (By.XPATH, f"//*[@id='match-card-{match_id}']//button[contains(@id, '{match_id}-{selection}')]/span[contains(@class, 'Value')]")

    def specific_match_team_names_locators(self, match_id):
        home_locator = (By.XPATH, f"((//*[@id='match-card-{match_id}']//span[contains(@class, 'teamName')])[1])")
        away_locator = (By.XPATH, f"((//*[@id='match-card-{match_id}']//span[contains(@class, 'teamName')])[2])")
        return home_locator, away_locator

    """ Match List Page Methods """

    def is_match_list_visible(self):
        return self.is_visible(self.match_list_locator)

    def select_specific_match_outcome(self, match_id, selection):
        """Click the odds button (HOME='1', DRAW='X', AWAY='2') for a specific match """
        button_locator = self.specific_match_odds_button_locator(match_id, selection)
        self.click(button_locator)

    def get_specific_match_outcome_odds_value(self, match_id, selection):
        """ Get the odds value for a specific match and selection (HOME='1', DRAW='X', AWAY='2') """
        value_locator = self.specific_match_odds_value_locator(match_id, selection)
        value_text = self.get_text(value_locator)
        return str(value_text)
    
    def get_specific_match_teams_names(self, match_id):
        """ Get the home and away team names for a specific match """
        home_locator, away_locator = self.specific_match_team_names_locators(match_id)
        home_name = self.get_text(home_locator)
        away_name = self.get_text(away_locator)
        return home_name, away_name

    def get_random_match_card_id(self):
        """Find all match cards, pick a random one, return its match_id (id minus the 'match-card-' prefix)."""
        cards = self.driver.find_elements(*self.match_list_all_cards_locator)
        chosen = random.choice(cards)
        full_id = chosen.get_attribute("id")
        return full_id.removeprefix("match-card-")

