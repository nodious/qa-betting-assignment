import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from api.client import BettingAPI

""" UI FIXTURES """

@pytest.fixture
def driver():
    """Provides a fresh Chrome WebDriver per test, and quits it afterward"""
    options = Options()
    # options.add_argument("--headless=new")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

""" API FIXTURES """

@pytest.fixture
def api():
    """Provides a BettingAPI client (auth header already set from USER_ID)"""
    return BettingAPI()

@pytest.fixture
def current_balance(api):
    """Returns the user's current balance"""
    response = api.get_balance()
    return response.json()["balance"]

@pytest.fixture
def valid_match(api):
    """Returns a real match from the API"""
    matches = api.get_matches().json()
    return matches[0]