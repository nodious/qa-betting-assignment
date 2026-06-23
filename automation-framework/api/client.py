""" Client wrapper for betting API. Endpoints documented at /api/docs (Swagger) """

import requests
from config import settings


class BettingAPI:
    MATCHES_ENDPOINT = "/api/matches"
    PLACE_BET_ENDPOINT = "/api/place-bet"
    BALANCE_ENDPOINT = "/api/balance"
    RESET_BALANCE_ENDPOINT = "/api/reset-balance"
    
    def __init__(self, user_id: str | None = None):
        self.base_url = settings.BASE_URL
        self.session = requests.Session()
        # The API authenticates via the x-user-id header (spec 5.1).
        self.session.headers.update({"x-user-id": user_id or settings.USER_ID})

    def get_matches(self):
        """GET /api/matches — returns the match list"""
        return self.session.get(f"{self.base_url}{self.MATCHES_ENDPOINT}")

    def place_bet(self, match_id, selection, stake):
        """POST /api/place-bet — places one bet"""
        payload = {"matchId": match_id, "selection": selection, "stake": stake}
        return self.session.post(f"{self.base_url}{self.PLACE_BET_ENDPOINT}", json=payload)

    def get_balance(self):
        """GET /api/balance — returns the user's balance"""
        return self.session.get(f"{self.base_url}{self.BALANCE_ENDPOINT}")
    
    def reset_balance(self):
        """POST /api/reset-balance — resets the user's balance. No payload required."""
        return self.session.post(f"{self.base_url}{self.RESET_BALANCE_ENDPOINT}")
