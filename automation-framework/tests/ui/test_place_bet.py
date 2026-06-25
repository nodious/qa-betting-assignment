"""
E2E UI test for the single bet placement happy path (MT-001).

Drives a full user journey: open the app, pick a match, select an outcome,
enter a stake, place the bet, and verify the success receipt and balance.

Chosen for automation because placing a bet is the core journey of the
product and exercises the most integration points (match list - bet slip -
placement - receipt - balance update) in a single flow.

Marked xfail (strict): the happy path cannot pass at the moment 
because of two confirmed defects it always hits —
  - BUG-002: Balance not being deducted after placing a bet on UI
  - BUG-011: Success Receipt Potential Payout is miscalculated
The test is expected to fail on the first of defect it reaches. 
If the build is fixed it will xpass, which
strict mode surfaces as a failure prompting the test to be updated.

A separate topic is BUG-010: Success Receipt does not show Bet Selection.
As the locator for selection in the receipt is not present in the DOM, this test cannot verify it.
This is the reason why this assertion is not included in this test, 
and the selection is verified on the bet slip instead.
"""


import pytest
import random
from pages.match_list_page import MatchListPage
from pages.bet_slip_page import BetSlipPage
from pages.header_page import HeaderPage
from pages.bet_receipt_modal_page import ReceiptModal

STAKE = "1.01"
SELECTION = ("home", "draw", "away")

@pytest.mark.ui
@pytest.mark.xfail(
    reason="Happy path cannot fully pass against current build — hits multiple confirmed defects: "
           "BUG-002 (balance not deducted), BUG-011 (receipt payout miscalculated), "
           "and BUG-012 (receipt reverses home/away team order)",
    strict=True,
)
def test_place_bet_happy_path(driver):
    """POM Setup"""
    match_list = MatchListPage(driver)
    bet_slip = BetSlipPage(driver)
    header = HeaderPage(driver)
    receipt = ReceiptModal(driver)

    """Match List"""
    match_list.open()
    assert match_list.is_match_list_visible()
    assert header.is_header_visible()
    assert header.is_header_brand_visible()
    starting_balance = header.get_balance()

    winner_selection = random.choice(SELECTION)
    match_id = match_list.get_random_match_card_id()
    expected_home, expected_away = match_list.get_specific_match_teams_names(match_id)
    expected_odds = match_list.get_specific_match_outcome_odds_value(match_id, winner_selection)

    match_list.select_specific_match_outcome(match_id, winner_selection)

    """Bet Slip"""
    assert bet_slip.is_bet_slip_visible()

    slip_home, slip_away = bet_slip.get_teams_names()
    assert (slip_home, slip_away) == (expected_home, expected_away), \
        f"Bet slip teams {(slip_home, slip_away)} != selected match {(expected_home, expected_away)}"
    assert bet_slip.get_match_winner() == winner_selection, \
        f"Bet slip selection '{bet_slip.get_match_winner()}' != selected '{winner_selection}'"
    assert bet_slip.get_odds_value() == float(expected_odds), \
        f"Bet slip odds {bet_slip.get_odds_value()} != match odds {expected_odds}"

    bet_slip.enter_stake(STAKE)
    expected_payout = round(float(STAKE) * float(expected_odds), 2)
    assert bet_slip.get_potential_payout() == expected_payout, \
        f"Bet slip payout {bet_slip.get_potential_payout()} != stake*odds {expected_payout}"

    bet_slip.place_bet()
    assert bet_slip.is_placing_indicator_visible()
    assert bet_slip.wait_until_placing_indicator_gone()

    """Receipt Modal"""
    assert receipt.is_displayed()

    assert receipt.get_bet_id()
    receipt_home, receipt_away = receipt.get_match()

    # BUG-012: this assertion fails — home/away teams are reversed in the receipt (receipt shows "Away vs Home")
    assert (receipt_home, receipt_away) == (expected_home, expected_away), \
        f"Receipt match {(receipt_home, receipt_away)} != selected {(expected_home, expected_away)}"

    assert receipt.get_stake() == float(STAKE), \
        f"Receipt stake {receipt.get_stake()} != entered {STAKE}"
    assert receipt.get_odds_value() == float(expected_odds), \
        f"Receipt odds {receipt.get_odds_value()} != selected odds {expected_odds}"
    assert receipt.get_timestamp()

    # BUG-011: this assertion fails — receipt payout is miscalculated (stake * 2, ignoring odds)
    assert receipt.get_payout() == expected_payout, \
        f"Receipt payout {receipt.get_payout()} != stake*odds {expected_payout} (BUG-011)"

    receipt.close()
    new_balance = header.get_balance()

    # BUG-002: this assertion fails — the UI does not deduct the stake
    assert new_balance == round(starting_balance - float(STAKE), 2), \
        f"Balance not deducted: was {starting_balance}, now {new_balance}, " \
        f"expected {round(starting_balance - float(STAKE), 2)} (BUG-002)"