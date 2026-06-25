# QA Engineer Home Assignment — Single Bet Placement

This repository contains my submission for the QA Engineer home assignment,
covering manual test strategy, automation, and scaling recommendations for the
single bet placement feature of the test betting application.

## Repository Structure

| Folder | Part | Contents |
|--------|------|----------|
| `manual-qa/` | Part A | Test plan (prioritized scenarios) and bug reports from execution & exploratory testing |
| `automation-framework/` | Part B | Automation project: framework, an E2E UI test, and an API validation test |
| `strategy-and-recommendations/` | Part C | Test selection rationale and recommendations for scaling |

Each folder is self-contained. Part B (automation) is the only part with
runnable code; setup and run instructions are below.

## Application Under Test

- Test application: `https://qae-assignment-tau.vercel.app/`
- API docs (Swagger): `https://qae-assignment-tau.vercel.app/api/docs`

---

## Automation Framework (Part B)

### Prerequisites
- Python 3.12+
- Latest desktop Chrome

### Installation

1. Clone the repository and enter the automation project

   ```
   git clone https://github.com/nodious/qa-betting-assignment.git
   cd qa-betting-assignment/automation-framework
   ```

2. Create and activate a virtual environment

   ```
   python3.12 -m venv venv
   source venv/bin/activate        # macOS/Linux
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

### Configuration

The suite authenticates to the test application using a `user-id`, supplied as
an environment variable rather than hardcoded, so anyone can run the suite with
their own `user-id` and no credentials are committed to version control.

1. Copy the example environment file:

   ```
   cp .env.example .env          # macOS/Linux
   ```

2. Open `.env` and set your `user-id`:

   ```
   USER_ID=<your-user-id>
   ```

The `user-id` is the same value used to authenticate in the application URL
(appended as a query parameter), as described in the assignment. `.env` is
gitignored and is not committed.

### Running the tests

1. API Automation:

   ```
   pytest tests/api/test_sports_betting.py -m api -v     # verbose for parametrized test case
   ```

2. UI Automation

   ```
   pytest tests/ui/test_place_bet.py -m ui               # throwback for errors: --tb=long
   ```

3. All tests

   ```
   pytest -v
   ```
