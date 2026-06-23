# Test Plan

## Note: for boundaries in tests below I have used actual acceptable values by the UI. There is a discrepancy between the System and the Feature Specification that states "Minimum €1.01 (positive values)". This discrepancy is something we should resolve - I mention it in the Strategy and Recommendations part. After resolving that requirement, tests/feature spec should get updated accordingly.

### ID: MT-001   Title: Single Bet Placement - Happy Path
- Priority: Critical
- Risk Rationale: End-to-end coverage of the System's crucial functionality
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches and a Balance that allows for bet placements
1. User selects a random bet by clicking '1', 'X', or '2' button on any match available     //      Bet slip with correct selection summary shows up on the right side of the screen as a fixed card
2. User inputs a correct Stake (between 1.00-100.00 euros) within their Balance range with 2-decimal precision (for example: 12.23 euros)     //   User is not presented with any validation error upon Stake placement, Place Bet button is actionable and green, 2-decimal values are accepted
3. User clicks Place Bet button      //      Upon clicking, Place Bet button becomes not actionable, and the text on the button changes to "Placing..."
4. User is presented with Success Receipt modal       //      Success Receipt shows correct bet details, unique bet ID, date of bet, success header, 'X' and Close button
5. User clicks 'X' or Close button      //      Success Receipt modal closes, User returns to Upcoming Football Matches screen

### ID: MT-002   Title: Single Bet Selection and Bet Slip Update - Validation
- Priority: High
- Risk Rationale: Ensuring feature's boundaries and that the User is able to place the bet they actually selected
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches
1. User selects a random bet        //      Bet slip with correct selection summary shows up on the right side of the screen as a fixed card
2. User tries to select another bet     //      Bet slip updates with correct selection summary from step 2, Single Bet is updated, System does not allow for multi betting

### ID: MT-003   Title: Stake Boundaries - Validation/Negative
- Priority: High
- Risk Rationale: Ensuring feature's boundaries/requirements and that the User is able to place the bet they actually selected
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches and a Balance that allows for bet placements
1. User selects a random bet        //      Bet slip with correct selection summary shows up on the right side of the screen as a fixed card
2. User inputs a correct Stake (between 1.00-100.00 euros) within their Balance range     //   User is not presented with any validation error upon Stake placement, Place Bet button is actionable and green
3. User inputs a boundary Stake value of 1.00 euro      //      User is not presented with any validation error upon Stake placement, Place Bet button is actionable and green
4. User inputs a boundary Stake value of 100.00 euro     //      User is not presented with any validation error upon Stake placement, Place Bet button is actionable and green 
5. User inputs Stake outside of feature's boundaries - below 1.00 euro - 0.99 and then other values      //      Validation error 'Minimum stake is €1.00' is shown below Stake input field,  Place Bet button is greyed-out and not actionable
6. User inputs Stake outside of feature's boundaries - above 100.00 euro - 100.01 and then other values      //      Validation error 'Maximum stake is €100.00' is shown below Stake input field,  Place Bet button is greyed-out and not actionable
7. User tries to input Stake with more than 2 decimal values (for example: 12.234 euros)        //      Stake field blocks any inputs after getting 2 decimal numbers

### ID: MT-004   Title: Date Filter - Validation
- Priority: Medium
- Risk Rationale: Ensuring high level of User Experience is important, but not as important as meeting technical requirements. Date and Odds filters are the only built-in solutions for filtering specific matches in current state of the System
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches
1. User opens Date Filter       //      Date: All selection is present, a calendar with current date view opens up, with All/Custom tabs, Reset, Cancel and Apply buttons present. Default selection: current date
2. User searches for a specific date (or range of dates) to filter the upcoming matches and presses Apply     //      Date (or range of dates) appears in Date selection, calendar view closes, Upcoming Football Matches list state updates to show only games in selected dates, with "Showing XX matches" summary text updating to the correct count of games present
3. User opens Date Filter again and Resets the filter      //      Upcoming Football Matches list state return to default stage, with "Showing XX matches" summary text updating to the correct count of games present

### ID: MT-005   Title: Odds Filter - Validation
- Priority: Medium
- Risk Rationale: Ensuring high level of User Experience is important, but not as important as meeting technical requirements. Date and Odds filters are the only built-in solutions for filtering specific matches in current state of the System
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches
1. User opens Odds Filter       //      Odds range filter view opens up, with a slider present that shows min and max values for odds and current selections for both - default: min - 1,00; max - 10,00. Reset and Apply buttons are present on Odds Filter view
2. User selects a specific Odds range and presses Apply         //       Odds range appears in Odds selection, odds filter view closes, Upcoming Football Matches list state updates to show only games with selected odds, with "Showing XX matches" summary text updating to the correct count of games present
3. User opens Odds Filter again and Resets the filter      //      Upcoming Football Matches list state return to default stage, with "Showing XX matches" summary text updating to the correct count of games present

### ID: MT-006   Title: Stake Exceeding Available Balance - Validation/Negative
- Priority: High
- Risk Rationale: Insufficient balance is a core financial guardrail - placing bets beyond available funds would let users wager money they do not have, with direct monetary consequences. Validating this rule protects both the user and the business.
- Steps     //      Expected Results:
Precondition: User is logged into the System with a Balance lower than the Stake they are about to input. The Balance available needs to be below 100 euros and above 1 euro
1. User selects a random bet        //      Bet slip with correct selection summary shows up on the right side of the screen as a fixed card
2. User inputs a Stake value that exceeds their available Balance      //      Validation error 'Insufficient balance' is shown below Stake input field, Place Bet button is greyed-out and not actionable
3. User attempts to place the bet      //      Placement is blocked - bet is not placed, no Stake is deducted, no Success Receipt is shown

#### Note: This scenario was initially blocked: on the first day of testing the balance was fixed at €125.50, above the €100.00 max stake, making the insufficient-balance state unreachable. On a subsequent day the balance had changed to €63.17 with no action taken by the tester, which made the scenario reproducible (a stake between €63.18–€100.00 exceeds balance while staying within the allowed stake range). The balance therefore appears to change between sessions/days in a way not described in the spec, which makes this scenario's executability environment-dependent and non-deterministic. Expected Results above reflect the day it was testable. This variability is raised in the Strategy and Recommendations section as a test-data control concern.

### ID: MT-007   Title: Bet Placement Failure - Error Modal Handling
- Priority: High
- Risk Rationale: The failure path is half of the placement outcome (success or failure) defined in the spec. If a bet fails, the user must be clearly informed and given a way to recover - a silent or broken failure could lead to lost bets, duplicate placements, or financial discrepancies.
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches and a Balance that allows for bet placements. User opens a second window and logs in again - the System is now active on two separate instances
1. User selects a random bet and inputs a valid Stake on both instances     //      Bet slip shows correct selection summary, Place Bet button is actionable and green on both instances
2. User clicks Place Bet button on both instances in quick succession and the placement fails (bet already in progress)      //      For one of the instances: Error modal appears with title 'Something went wrong', body explaining the bet could not be processed and suggesting to try again, with Rebet, Close and top-right 'X' actions present ; For the other instance: Bet placed successfully
3. User clicks Rebet on the failed instance modal      //      Modal closes and placement is retried
4. User triggers the failure again and clicks Close (or top-right 'X')      //      Modal closes and current selection/Stake is cleared, User returns to main flow

#### Note: The failure state was reached by opening the application in two windows and submitting both placements simultaneously, exploiting the brief Placing... window to trigger a "bet already in progress" style conflict (spec API error class 409). The error modal ("Something went wrong", with Rebet/Close/X) appeared and was verified. Note that this trigger is manual and timing-dependent — there is no straightforward, deterministic UI mechanism to induce a placement failure on demand. For reliable, repeatable coverage, the documented API error classes (400/401/405/409/422/500) are better verified directly against the place-bet endpoint, which is where this is addressed in automation.