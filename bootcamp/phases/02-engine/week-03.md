---
week: 3
phase: P2
title: Build the Accounting Machine
deliverables: [D05, D06]
concepts: [C05, C06, C07]
milestone: null
hours: 16-20
---

# Week 3 — Build the Accounting Machine

## Learning objective

Ship an event-driven backtester that turns target weights into fills, cash and an equity curve without ever using information from the future - and prove it by reproducing buy-and-hold within 1%.

## Deliverable

- [D05 — Backtester v1](deliverables/D05.md): `engine/backtest.py` with the event loop, next-bar fills, cash and position tracking, plus passing engine tests.
- [D06 — Cost model + cost sensitivity report](deliverables/D06.md): `engine/costs.py` wired into the loop, and `reports/cost-sensitivity.md`.

The reference implementation you are replacing is `kit/spine.py`; the interface you must match is in [spec/engine-spec.md](spec/engine-spec.md).

## Daily tasks

### Mon — Read the reference, then write your interface

1. Read `kit/spine.py` end to end (about 400 lines). Write down, in your own words, the four contracts it implements.
2. Read [spec/engine-spec.md](spec/engine-spec.md) and list the behaviours your engine must reproduce: next-bar execution, turnover accounting, artifact layout, fingerprints.
3. Sketch `engine/backtest.py`: the event loop, the data structures, and where costs enter. No code beyond function signatures today.

*Time: 2-3 h. Expect the temptation to start coding immediately; resist it - the interface is the deliverable.*

### Tue — Event loop v0: ugly, runs, produces an equity curve

1. Implement the loop: iterate bars, read target weights, compute returns, compound equity.
2. Get ONE number out: final equity for constant weight 1.0 on SPY.
3. Compare with buy-and-hold from Week 1. They should match to within a rounding error. If they do not, you have found your first engine bug - write down what it was.

*Time: 4-5 h. Expect: a factor-of-two error from weights being applied to the wrong bar. That is the classic first bug.*

### Wed — Positions, cash and the time-travel test (D05 core)

1. Track positions explicitly (weights are not positions): quantity, value, cash.
2. Implement `state_at(date)` and use it for the time-travel test: run the engine on data truncated at date T, and on the full sample. Positions up to T must be **identical**.
3. Inject [C05 — Annualization](concepts/C05-annualization.md): your engine prints daily numbers; every comparison you care about is annual.

*Time: 3-4 h. The time-travel test is the single most valuable 10 lines of the whole phase.*

### Thu — Metrics you can defend (C06, C07)

1. Implement `engine/metrics.py` with `vol`, `sharpe`, `sortino` - and run `kit/tests/test_metrics.py` against your versions (copy the relevant tests into `tests/test_metrics.py` and import your module).
2. Inject [C06 — Volatility & Standard Deviation](concepts/C06-volatility-and-std-dev.md) and [C07 — Sharpe Ratio](concepts/C07-sharpe-ratio.md).
3. Annualisation: prove to yourself that daily vol × √252 is right by simulating daily returns from a known annual vol.

*Time: 4-5 h. Expect: your Sharpe to be wrong by √252 the first time. Everyone's is.*

### Fri — Costs enter the engine (D06)

1. Implement `engine/costs.py`: `cost = turnover × (fee_bps + slippage_bps) / 10000`, charged in the loop, not in the report.
2. Inject [C10 — Transaction Costs & Slippage](concepts/C10-transaction-costs-and-slippage.md) (first half: the mechanics; the report is Saturday).
3. Run one strategy at 0, 5, 10, 20 bps. Plot the equity curves. Find the breakeven.

*Time: 3-4 h. Expect: a strategy that looked fine at 0 bps to lose money at 20.*

### Sat — The look-ahead experiment: quantify your own cheating

1. Run a momentum rule two ways: with `signal_shift=1` (honest) and `signal_shift=0` (cheating). Record the gap in Sharpe and return.
2. Run the time-travel test suite from [lookahead/](lookahead/lookahead-test-suite.md).
3. Write `reports/cost-sensitivity.md`: the bps grid table, the breakeven cost, and one paragraph on what turnover actually costs your rule per year.

*Time: 3-4 h.*

### Sun — Tests green, artifacts saved, journal, gate

1. `make test-contract E=engine.backtest` must pass - your engine against the same suite the reference passes.
2. `make run E=engine.backtest S=<spec> NAME=engine-v1` produces the four artifacts. Compare with the same run through `kit.spine`: numbers should agree to within rounding.
3. Document the engine in `engine/README.md` (the Week 3 gate requires it), journal, update the graveyard if a strategy died.

*Time: 2-3 h.*

## Gate

`make gate WEEK=3` - see [gates/week-03-gate.md](gates/week-03-gate.md). The two mechanical requirements that matter most: your engine passes the contract suite, and buy-and-hold reproduces within 1%.

## Graveyard prompt

Your v0 engine was wrong. Keep its equity curve and the bug description: it is the exhibit for the concept file on look-ahead you will write in Week 4. Also log any strategy that died when costs were switched on - with the breakeven bps, because that number is the strategy's real personality.

## Concept injections this week

- [C05 — Annualization](concepts/C05-annualization.md) — triggered by daily numbers and annual comparisons
- [C06 — Volatility & Standard Deviation](concepts/C06-volatility-and-std-dev.md) — triggered by wanting to know if 1.2%/day is a lot
- [C07 — Sharpe Ratio](concepts/C07-sharpe-ratio.md) — triggered by two equity curves ending in the same place
- [C10 — Transaction Costs & Slippage](concepts/C10-transaction-costs-and-slippage.md) — triggered by a strategy dying at 10 bps
