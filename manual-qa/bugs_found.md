# Bug Report

### ID: BUG-001   Title: Past games present under Upcoming Football matches, Users able to bet on Past Matches
- Severity: Critical
- Steps to reproduce:
1. Log in with authenticated User account and view Upcoming Football Matches list
2. Look for Football Matches with tag other than 'UPCOMING' - like 'PAST'
3. Try to place a bet on Past Matches
- Expected Result: Only upcoming football matches are present in the list and only upcoming games can be bet upon
- Actual Result: Both past and upcoming football matches are present in the list and users are able to place bets on past games
- Business Impact: Huge business impact, as users are able to place invalid bets for games that already took place - the results are known, so there is a lot of money that can be lost. User experience is also struck by this, as users will be disoriented with the view.
- Evidence: "PAST" tag next to matches in the Upcoming Footbal Matches list

### ID: BUG-002   Title: Balance not being deducted after placing a bet on UI
### Note: I am aware this is done on purpose for this recruitment demo app, but still - that would be a massive bug on live application
###       API calls to place-bet endpoint reduce the balance correctly, which confirms the bug is UI-side only
- Severity: Critical (in production environment)
- Steps to reproduce:
1. Log in with authenticated User account and view Upcoming Football Matches list
2. Select a random bet, place a bet with random Stake withing account's balance
- Expected Result: Stake amount is deducted from account's Balance upon successfull bet placement
- Actual Result: Stake amount is not being deducted from account's Balance upon successfull bet placement
- Business Impact: Huge business impact, as users are able to place  bets without their balance actually being deducted, so there is a lot of money that can be lost. User experience is also struck by this, as users will be disoriented with the System behaviour.
- Evidence: Balance not updating after placing bet

### ID: BUG-003   Title: „Showing XX matches” shows incorrect count of matches
- Severity: Medium
- Steps to reproduce:
1. Log in with authenticated User account and view Upcoming Football Matches list
2. Filter the list in any way, so that the list count updates
- Expected Result: „Showing XX matches” updates count accordingly to the list state
- Actual Result: „Showing XX matches” is static - it always says 'Showing 103 matches'
- Business Impact: Not that big, but can be misleading. User experience is also struck by this, as users will be disoriented with the wrong information it provides.
- Evidence: filtering for just one date with a single match still shows 'Showing 103 matches'

### ID: BUG-004   Title: Reset on Date Filter does not reset date calendar to current date view
- Severity: Medium
- Steps to reproduce:
1. Log in with authenticated User account and view Upcoming Football Matches list
2. Open Date Filter view, go back/forth a few months, select a date and Apply
3. Open Date Filter view again, press Reset
- Expected Result: Upcoming Football Matches list updates upon resetting the Date Filter and the Calendar view on Date Filter view resets to show current date selection
- Actual Result: Upcoming Football Matches list updates upon resetting the Date Filter and the Calendar view on Date Filter view does not reset to show current date selection
- Business Impact: Minimal. User experience is struck by this, as users would have to navigate manually over and over in the calendar.
- Evidence: go back a few months and then press Reset. The Calendar does not reset to show current date

### ID: BUG-005   Title: Bet slip moves slightly upwards when scrolling down instead of staying fixed
- Severity: Low
- Steps to reproduce:
1. Log in with authenticated User account and view Upcoming Football Matches list
2. Press any bet
3. Scroll down the list of Upcoming Football Matches with Bet Slip open
- Expected Result: Bet slip stays fixed and scrolling does not affect it's position on screen
- Actual Result: Bet slip moves slightly upwards upon initial scroll down
- Business Impact: None. Minor visual bug.
- Evidence: Scroll slowly once - you will see Bet Slip moving up a bit. After initial scroll Bet Slip stays fixed. It has something to do with the main grid container element.

### ID: BUG-006   Title: Stake exceeding available balance is accepted, resulting in negative balance
- Severity: Critical
- Steps to reproduce:
1. Log into Swagger and authenticate with unique user ID
2. POST a bet using /api/place-bet that exceeds current balance
- Expected Result: Placement is rejected with an 'Insufficient balance' error (spec 4.1); Balance never drops below €0.00; no further bets are possible once Balance is insufficient and all return similar error.
- Actual Result: The bet is accepted, the Balance becomes negative, and further bets can still be placed despite a negative Balance
- Business Impact: Critical financial failure. Users can wager money they do not have, driving the account into negative balance with no consequence. On a live system this is a direct financial loss - a user could place unlimited bets with no funds. It also breaks the core 'cannot exceed available balance' business rule that protects both user and operator.
- Evidence: place-bet API returns HTTP 200 with a negative "balance" value for a stake exceeding available funds; subsequent placements continue to succeed.

### ID: BUG-007   Title: Place-bet API returns currency "USD" instead of "EUR"
- Severity: High
- Steps to reproduce:
1. Log into Swagger and authenticate with unique user ID
2. Place any valid bet (e.g. matchId premier-league-manutd-chelsea, selection HOME, stake €10)
3. Inspect the place-bet API response
- Expected Result: The "currency" field returns "EUR", consistent with the Feature Specification
- Actual Result: The "currency" field returns "USD" (GET /api/balance response returns "EUR")
- Business Impact: Currency mismatch in a financial discrepancy that can lead to a financial loss. Causes user confusion, incorrect financial reporting, and potential discrepancies if any downstream system acts on the currency code.
- Evidence: place-bet 200 response body contains "currency": "USD" despite all stake/payout values being defined in EUR.

### ID: BUG-008   Title: Reset-balance API returns static "balance": 125.5
- Severity: High
- Steps to reproduce:
1. Log into Swagger and authenticate with unique user ID
2. Reset balance using /api/reset-balance endpoint
3. Inspect the reset-balance API response
- Expected Result: The "balance" field returns an actual account balance
- Actual Result: The Reset-balance API returns static "balance": 125.5
- Business Impact: Not that high, unless balance state visible for users is pulled from reset-balance (which is unlikely). If that would be the case - the account balance would be incorrect, which would cause a huge business impact. Luckily, the GET /api/balance works correctly and UI seems to be pulling data from it.
- Evidence: Discrepancy between /api/reset-balance endpoint response balance and /api/balance GET response balance

### ID: BUG-009   Title: Non-numeric / malformed stake values cause HTTP 500 instead of graceful 422 error
- Severity: High
- Steps to reproduce:
1. Log into Swagger and authenticate with unique user ID
2. POST to /api/place-bet with a valid matchId and selection, and a malformed stake value:
   - a non-numeric string, e.g. "asd" or
   - a number using a comma as a decimal separator, e.g. "1,23"
- Expected Result: The API rejects the invalid stake gracefully with HTTP 422 and a validation error (spec 4.1: "Stake must be numeric → Reject non-numeric values")
- Actual Result: The API returns HTTP 500 Internal Server Error, indicating an unhandled exception rather than input validation
- Business Impact: Malformed user input crashes the request handler instead of being rejected gracefully. A 500 indicates the input validation layer is incomplete and an exception is reaching the server. 500 errors can be a security risk so the business impact here is quite significant.
- Evidence: POST /api/place-bet with stake "asd" or "1,23" returns HTTP 500; valid and other invalid-but-handled stakes (e.g. 0.99) return 422 as expected.