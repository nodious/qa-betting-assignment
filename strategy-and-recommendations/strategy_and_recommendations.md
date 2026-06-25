# Part C — Strategy & Recommendations

## Why these two tests were automated

I automated one **E2E UI test** (the single-bet happy path) and one **API validation test**
(parametrized stake validation), because together they cover the two highest-value, most
distinct risk areas with the least overlap.

- **UI happy path (E2E):** placing a bet is the core journey and touches the most
  integration points in one flow — match list → bet slip → placement → receipt → balance.
  Automating the critical path first gives the most confidence per test, and it surfaced
  several defects a thinner check would miss (receipt payout, team order, balance deduction).

- **API stake validation (parametrized):** the business rules around stake (min, max, precision)
  are fast, and stable — ideal for automation. Driving the `place-bet` endpoint
  directly tests the rules at their source, independent of UI state, and a single parametrized
  test cleanly covers multiple inputs (and documents malformed-input defects via `xfail`).

Other candidates (filters, the error-modal flow) were lower priority: either
lower business impact, or — like the error modal — not reliably triggerable on UI, which makes them a
poor fit for automation right now.

## What was intentionally left as manual / not automated

- **Insufficient-balance validation:** designed but not built as a test. It is a known defect
  (BUG-006: over-balance stakes are accepted, allowing a negative balance). 
  Reaching the state reliably is also tricky: the
  balance is not controlled by the tester, varies between sessions, and the reset endpoint is itself
  unpredictable. Given the assignment scope (one API test), it is documented in the bug report and
  noted in code rather than implemented.

- **Filters and bet-slip actions:** suitable for automation later, but lower-risk than the core
  placement flow, so they were kept as manual/exploratory checks for this submission.

- **Error-modal / failure path:** reproducible only via a manual timing race (concurrent
  placement), with no visible UI trigger. Better verified at the API layer.

## Recommendations to scale

1. **Controllable test data.** The single biggest blocker. The balance is not
   settable to a known value, changes between sessions (seems to happen daily), 
   and the reset endpoint is unreliable. Reliable validation testing needs the ability 
   to seed a user to a known balance and reset state cleanly between tests —
   otherwise tests pass or fail based on whatever the balance happens to be that day.

2. **CI/CD with layered execution.** Run the suite on every push, splitting fast API tests
   (`pytest -m api`, no browser) from the slower browser-based UI tests so feedback stays quick.
   The existing `xfail` markers serve as regression guards: when a documented bug is
   fixed, strict mode flags it (`xpass`) so the test gets updated.

3. **Failure-injection + spec clarifications.** Add a mechanism to
   force API error responses on demand, so the error-modal and failure paths can be tested
   manually on UI instead of via timing races. Separately, the spec has gaps worth resolving
   before broadening coverage — e.g. the €1.00 vs €1.01 minimum-stake inconsistency, and the
   receipt omitting the Selection field that section 2.4 requires.