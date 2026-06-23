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
- Status: NOT EXECUTED in Part A - see note below
- Risk Rationale: Insufficient balance is a core financial guardrail - placing bets beyond available funds would let users wager money they do not have, with direct monetary consequences. Validating this rule protects both the user and the business.
- Steps     //      Expected Results:
Precondition: User is logged into the System with a Balance lower than the Stake they are about to input
1. User selects a random bet        //      Bet slip with correct selection summary shows up on the right side of the screen as a fixed card
2. User inputs a Stake value that exceeds their available Balance      //      Validation error 'Insufficient balance' is shown below Stake input field, Place Bet button is greyed-out and not actionable
3. User attempts to place the bet      //      Placement is blocked - bet is not placed, no Stake is deducted, no Success Receipt is shown

#### Note: This scenario could not be executed during Part A. The demo environment provides a fixed Balance of €125.50 and a maximum Stake of €100.00, which makes the insufficient-balance state unreachable through the UI - the maximum allowed Stake is always lower than the available Balance. This path is additionally closed by BUG-002 (Balance is not deducted after placing a bet), so the Balance cannot be drained through repeated placements either. The scenario is designed against the Feature Specification (section 4.1) and will be covered through API automation, where a stake-exceeds-balance request can be sent directly to the place-bet endpoint and the rejection response verified. This is also raised in the Strategy and Recommendations part as a test-data limitation.


### ID: MT-007   Title: Bet Placement Failure - Error Modal Handling
- Priority: High
- Status: NOT EXECUTED in Part A - see note below
- Risk Rationale: The failure path is half of the placement outcome (success or failure) defined in the spec. If a bet fails, the user must be clearly informed and given a way to recover - a silent or broken failure could lead to lost bets, duplicate placements, or financial discrepancies.
- Steps     //      Expected Results:
Precondition: User is logged into the System and has access to Upcoming Football Matches and a Balance that allows for bet placements
1. User selects a random bet and inputs a valid Stake      //      Bet slip shows correct selection summary, Place Bet button is actionable and green
2. User clicks Place Bet button and the placement fails (server-side failure)      //      Error modal appears with title 'Something went wrong', body explaining the bet could not be processed and suggesting to try again, with Rebet, Close and top-right 'X' actions present
3. User clicks Rebet      //      Modal closes and placement is retried
4. User triggers the failure again and clicks Close (or top-right 'X')      //      Modal closes and current selection/Stake is cleared, User returns to main flow

#### Note: This scenario could not be executed during Part A. The demo environment provides no mechanism to force a placement failure through the UI - every valid placement resolves to success, and there is no way to induce a server-side error (500), a bet-already-in-progress conflict (409), or other failure from the interface. The scenario is designed against the Feature Specification (section 2.5) and will be approached through API automation, where the documented errors can be triggered and verified directly against the place-bet endpoint. This is also raised in the Strategy and Recommendations part.