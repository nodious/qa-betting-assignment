"""
API validation tests for the place-bet endpoint.

Verifies the API stake validation by sending invalid
stakes directly to /api/place-bet and asserting the documented rejection.
Chosen for automation because the POST place-bet endpoint is the most critical endpoint if it comes to its functionality.

NOTE — Insufficient-balance validation (422) was intentionally not implemented as a case in test_stake_validation_is_rejected_422. 
It requires an extra logic loop, that resets the balance to a known value before each test, get the balance (BUG-008) 
and then place a bet with a stake greater than the balance. If the balance is higher than 100 euros, we need to loop this logic 
until we get a balance lower than 100 euros, which is the maximum stake allowed.

Since I had to build one API test case for this exercise, I decided to build a more robust test case that covers more cases of stake validation.
"""

import pytest
import random

SELECTIONS = ("HOME", "DRAW", "AWAY")

@pytest.mark.api
@pytest.mark.parametrize("stake_param, expected_error", [
    (0.99, "invalid_stake_min"),
    (100.01, "invalid_stake_max"),
    (1.123, "invalid_stake_precision"),
    pytest.param("asd", "invalid_stake", marks=pytest.mark.xfail(
        reason="BUG-009: Non-numeric / malformed stake values cause HTTP 500 instead of graceful 422 error")),
    pytest.param("1,23", "invalid_stake", marks=pytest.mark.xfail(
        reason="BUG-009: Non-numeric / malformed stake values cause HTTP 500 instead of graceful 422 error")),
])
def test_stake_validation_is_rejected_422(api, valid_match, stake_param, expected_error):
    response = api.place_bet(
        match_id=valid_match["id"],
        selection=random.choice(SELECTIONS),
        stake=stake_param,
    )

    assert response.status_code == 422, f"Expected status code 422 for stake {stake_param}, got {response.status_code}"
    assert response.json()["error"] == expected_error, f"Expected error '{expected_error}' for stake {stake_param}, got '{response.json()['error']}'"
