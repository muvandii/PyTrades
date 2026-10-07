---
week: 4
phase: P2
title: Costs, OOS, Tearsheets
deliverables: [D07]
concepts: [C08, C09, C10]
milestone: M2
hours: 16-20
---

# Week 4 — Costs, OOS, Tearsheets

## Learning objective

Add out-of-sample discipline and automatic tearsheets to the engine, survive your own drawdowns, and pass milestone M2: any idea, data to verdict, in under 30 minutes.

## Deliverable

- [D07 — Walk-forward/OOS runner + tearsheets + look-ahead suite green](deliverables/D07.md): `engine/walkforward.py`, `engine/tearsheet.py`, `tests/test_lookahead.py`, and a tearsheet for one strategy with in-sample and out-of-sample columns.

## Daily tasks

### Mon — Drawdowns are the story (C08)

1. Print your best strategy's equity curve and mark the peak-to-trough declines. Compute max drawdown, its duration, and time-to-recovery.
2. Inject [C08 — Max Drawdown & Recovery](concepts/C08-max-drawdown-and-recovery.md).
3. Recompute the strategy's metrics on the drawdown window only. Ask: would you have kept running it?

*Time: 3-4 h. Expect to be surprised by duration: most real drawdowns are measured in years, not weeks.*

### Tue — Return vs pain (C09) and the tearsheet generator

1. Inject [C09 — Calmar & Return-vs-Pain](concepts/C09-calmar-and-return-vs-pain.md). Compute Calmar and Ulcer for two strategies with similar Sharpe.
2. Build `engine/tearsheet.py` producing the sections in `shared/templates/tearsheet.md`: headline, IS vs OOS, drawdown table, monthly grid, trade anatomy, cost sensitivity, fragility, and the "what this does not tell you" paragraph.

*Time: 4-5 h. The last section is why the generator is in the engine: it forces the caveats to travel with the numbers.*

### Wed — Walk-forward, the honest split (C15 comes in Week 6; today is mechanics)

1. Implement `splits()` per [spec/walkforward-splitter.md](spec/walkforward-splitter.md): rolling 3-year train, 6-month test, 1-bar embargo.
2. Add the pooled-OOS runner: optimise on train, evaluate on test, concatenate all test windows.
3. Run it for one strategy. Report per-split Sharpe, the degradation ratio, and the parameter-stability table.

*Time: 4-5 h. Expect: OOS Sharpe well below IS Sharpe. That gap is the most honest number in the course.*

### Thu — Look-ahead suite green (D07 core)

1. Write tests 1 and 2 from [lookahead/lookahead-test-suite.md](lookahead/lookahead-test-suite.md): time travel and signal-shift premium.
2. Run the shipped contract suite against your engine.
3. `reports/lookahead-audit.md`: both test results, the measured shift premium, and the blind-data paragraph (test 4).

*Time: 3-4 h.*

### Fri — M2 rehearsal: a fresh idea, timed

Take an idea you have not tested - something from a paper abstract, a podcast, or your own notes - and run it through today, cold: spec file, signal, `make run E=engine.backtest`, tearsheet, verdict. Time yourself, and write down every step that needed a manual fix.

*Time: 3-4 h. This is a rehearsal: the real M2 run happens Saturday or Sunday and must be under 30 minutes.*

### Sat — M2: the timed end-to-end run

1. Timer on. New idea, from raw data to tearsheet + written verdict, in under 30 minutes.
2. Log the timer and the step breakdown in `strategies/<id>/verdict.md` (or a `reports/cold-run-*.md` file referenced from it).
3. If you exceed 30 minutes, fix the friction you found, then repeat tomorrow with a second fresh idea.

*Time: 2-3 h including retries.*

### Sun — Verdict, graveyard, journal, gate

1. Finalise D07 artifacts: the tearsheet for your best strategy, the walk-forward report, the look-ahead audit.
2. Graveyard: which strategies died this phase, and of what (cost death, no edge after OOS)?
3. `make gate WEEK=4`. Milestone M2 passes only with the timed run documented.
4. Journal the phase-level question: what did building your own engine teach you that using someone else's would not have?

*Time: 2-3 h.*

## Gate

`make gate WEEK=4` - see [gates/week-04-gate.md](gates/week-04-gate.md). Milestone **M2: take a fresh idea from data to tearsheet + verdict in under 30 minutes.**

## Graveyard prompt

At least one strategy should die this week, and it should die of `cost death` or `no edge after OOS`. Record the breakeven cost and the IS-vs-OOS Sharpe gap. If nothing died, you did not test anything hard enough - go find the survivor's weakest assumption and attack it.

## Concept injections this week

- [C08 — Max Drawdown & Recovery](concepts/C08-max-drawdown-and-recovery.md) — triggered by a 40%+ drawdown in your own engine output
- [C09 — Calmar & Return-vs-Pain](concepts/C09-calmar-and-return-vs-pain.md) — triggered by two strategies with equal Sharpe and very different pain
- [C10 — Transaction Costs & Slippage](concepts/C10-transaction-costs-and-slippage.md) — completed last week, revisited here as the OOS killer

## After this week

Phase 3 runs the engine you just built, at volume: six strategy families, six verdicts, sensitivity heatmaps, and the first honest survivors. If your engine is slow, flaky, or unclear, fix it now - the factory will expose every weakness sixty times.
