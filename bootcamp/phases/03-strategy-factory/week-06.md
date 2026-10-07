---
week: 6
phase: P3
title: Six Strategies and an Honest Mirror
deliverables: [D10, D11]
concepts: [C14, C15]
milestone: M3
hours: 18-22
---

# Week 6 — Six Strategies and an Honest Mirror

## Learning objective

Extend the factory to three more families (Donchian, cross-sectional momentum, pairs), then attack your own best result with bootstrap, t-test, walk-forward and perturbation until it either survives or joins the graveyard.

## Deliverable

- [D10 — Strategies S04-S06 + bootstrap CIs](deliverables/D10.md): three more verdicts with confidence intervals.
- [D11 — Overfitting audit + sensitivity heatmaps](deliverables/D11.md): `reports/overfitting-audit.md` and the parameter grids behind it.

## Daily tasks

### Mon — S04 Donchian breakout

1. Implement `S04_donchian`: 20-day high entry, 10-day low exit, long-only on ETFs, optional ATR stop.
2. Run it, generate the tearsheet, and note the trade count: breakouts should trade more often than a 50/200 cross.
3. Compare with S01's tearsheet: same family, different patience.

*Time: 4-5 h.*

### Tue — S05 cross-sectional momentum

1. Implement `S05_momentum`: rank the universe by 12-1 month return monthly, hold the top 3, equal weight.
2. This is your first multi-asset, rank-based strategy: watch the universe requirement (min coverage) and how the engine handles monthly rebalancing.
3. Run with costs and note the turnover: monthly rebalancing of a 3-name book is cheap, and this strategy should survive on that ground.

*Time: 4-5 h.*

### Wed — S06 pairs (KO/PEP or your choice)

1. Implement `S06_pairs`: spread of two related names, z-score entry at ±2, exit at 0, 60-day formation window.
2. Run it. Then re-select the pair on the first half of the sample only and re-run on the second half - the honest version.
3. Inject [C18 — Cointegration & Spreads](../04-paper-replication/concepts/C18-cointegration-and-spreads.md) early if the spread looks like a trend on the full sample.

*Time: 4-5 h. Expect the pair to work beautifully in-sample and to stop working exactly where you needed it.*

### Thu — Bootstrap and t-test on your best survivor (C12 again, deeper)

1. For the best of S01-S06: block bootstrap the OOS Sharpe (2,000 resamples, block = holding period) and the mean return.
2. Inject [C14 — t-test Intuition](concepts/C14-t-test-intuition.md). Compute the t-stat of the strategy's mean daily return and interpret it against the number of *independent* bets.
3. Write `reports/bootstrap.md`: the CI, whether it excludes zero, and the honest sentence about what the CI does not cover (regime change, costs drift).

*Time: 4-5 h.*

### Fri — The overfitting audit (C15, D11)

1. Inject [C15 — Overfitting & Walk-Forward Honesty](concepts/C15-overfitting-and-walkforward.md).
2. Walk-forward every survivor with the Week 4 machinery: pooled OOS Sharpe, degradation ratio, parameter stability.
3. Build the two-parameter heatmaps (`reports/sensitivity/*.csv` for at least two strategies) and classify each surface: plateau, ridge, or spike.

*Time: 4-5 h.*

### Sat — The mirror: attack your own best result

Write `reports/overfitting-audit.md` answering, for your best strategy:

1. How many specifications did I try before this one? (Count them - be honest, it is the number that deflates your Sharpe.)
2. What is the OOS/IS Sharpe ratio? Below 0.5 means the IS number was mostly fitting.
3. Is the edge a plateau or a spike? Width of the plateau in parameter units?
4. Does it survive 2× my cost assumption?
5. Does it survive dropping its best year? Its best 5% of trades?
6. If a stranger read only `verdict.md`, would they know all five answers?

*Time: 4-5 h.*

### Sun — Milestone M3, journal, gate

1. `make gate WEEK=6`: six verdicts, 3+ graveyard entries, the audit, sensitivity data, bootstrap CI.
2. **M3 pass condition:** at least one survivor whose OOS Sharpe sits inside a bootstrap CI that excludes zero - or an honest statement that none do, with the graveyard to prove you tested.
3. Journal the phase: what pattern killed the most strategies?

*Time: 2-3 h.*

## Gate

`make gate WEEK=6` - see [gates/week-06-gate.md](gates/week-06-gate.md). Milestone **M3: 6 strategies tested, 3+ in the graveyard, at least one survivor with OOS evidence.**

## Graveyard prompt

This is the week the graveyard earns its keep. Six strategies, and a realistic split is four dead, one inconclusive, one survivor. Log the deaths with numbers: breakeven bps, OOS Sharpe, trade count. Then cluster them - how many died of the same cause? That cluster is what Phase 3's retro asks about, and it is what your Phase 5 risk rules must be designed against.

## Concept injections this week

- [C14 — t-test Intuition](concepts/C14-t-test-intuition.md) — triggered by needing a decision rule for "is this mean return real?"
- [C15 — Overfitting & Walk-Forward Honesty](concepts/C15-overfitting-and-walkforward.md) — triggered by IS Sharpe 2.1 and OOS Sharpe −0.2
