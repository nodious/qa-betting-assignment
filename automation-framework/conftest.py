import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from api.client import BettingAPI


@pytest.fixture
def driver():
    """Provides a fresh Chrome WebDriver per test, and quits it afterward."""
    options = Options()
    # options.add_argument("--headless=new")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def api():
    """Provides a BettingAPI client (auth header already set from USER_ID)."""
    return BettingAPI()