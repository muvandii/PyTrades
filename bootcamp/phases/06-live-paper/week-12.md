---
week: 12
phase: P6
title: Reconcile Reality
deliverables: [D17]
concepts: [C24, C25]
milestone: M5
hours: 14-18
---

# Week 12 — Reconcile Reality

## Learning objective

Explain every basis point of gap between your live paper PnL and your backtest's promise - and finish the course's hardest milestone: milestone **M5**, thirty days of live logs plus a reconciliation a stranger could check.

## Deliverable

- [D17 — 30-day live log + reconciliation report + divergence post-mortem](deliverables/D17.md): `live/equity.csv`, `live/reconciliation.md`, `live/postmortem.md`.

## Daily tasks

### Mon — Build the reconciliation properly

1. Rebuild the "shadow backtest": the same spec, same data, same window, same costs, run *as of* each live day (not one run over the whole window - the live bot decided each day with only the data available then, and your shadow must too).
2. Build the component table from `shared/templates/reconciliation.md`:

   | Component | Live (bps of notional or % of return) | Backtest | Gap | Cause |
   | --- | --- | --- | --- | --- |
   | Fees | | | | |
   | Slippage | | | | |
   | Timing (decision-to-fill) | | | | |
   | Missed/rejected fills | | | | |
   | Sizing differences | | | | |
   | Regime | | | | |
   | Unexplained | | | | |

3. Inject [C24 — Live vs Backtest Divergence](concepts/C24-live-vs-backtest-divergence.md): the taxonomy and the sign conventions that make the table add up.

*Time: 4-5 h.*

### Tue — Attribute the gap until "unexplained" is under 10%

1. Work the table: every unexplained basis point gets an investigation. Common culprits, in the order they usually appear: a decision-to-fill timing difference (your backtest fills at the next open; your bot fills at 07:12), a cost model that used the wrong side of the spread, a position drift you did not rebalance, a signal computed on adjusted vs unadjusted prices.
2. Record the investigation, not just the conclusion: "checked the fill timestamps; the 4 bps timing gap is 3 trading days where the order was submitted after the open" is a finding; "timing" is a label.
3. The honesty rule: if the unexplained bucket stays above 10%, say so in the report and list what you would need (tick data, order-level timestamps) to close it. Do not shrink the bucket by relabelling.

*Time: 4-5 h.*

### Wed — Regime, not bug (C25)

1. Inject [C25 — Regime Detection](concepts/C25-regime-detection.md).
2. Compute your live window's realised vol and your backtest's median vol. If the window was unusually quiet or unusually violent, quantify how much of the divergence is *expected* given the regime rather than the implementation.
3. Add the regime row to the reconciliation with a number: "expected divergence due to regime: X bps, computed by re-running the shadow backtest on the N nearest historical analogues".

*Time: 3-4 h.*

### Thu — The post-mortem (the honest document)

`live/postmortem.md`, using `shared/templates/reconciliation.md`'s post-mortem section:

1. Every operational failure, with timestamp and consequence.
2. Every mid-run rule change or manual intervention - each logged as a killed variant.
3. What you would change in the harness, in the risk policy, and in the strategy, ranked by expected bps of impact.
4. The expected-divergence budget for next month: "I expect live to trail the backtest by X bps/month, of which Y is structural".

*Time: 3-4 h.*

### Fri — M5 audit: does the evidence hold up?

Checklist for M5 (all must be true):

- [ ] 30+ rows in `live/equity.csv`, one per calendar trading day, no gaps unaccounted for
- [ ] A log file per day, including days with no orders
- [ ] The shadow backtest reproduces the live window's decisions day by day (spot check at least ten days by hand)
- [ ] `live/reconciliation.md` attributes divergence to named components with numbers
- [ ] `live/postmortem.md` lists failures and an expected-divergence budget
- [ ] The strategy traded is the one the spec fingerprint names - unchanged through the window
- [ ] If you are short of 30 days (clock started late), the report says so and the count to date

*Time: 4-5 h.*

### Sat — Pull the threads together for Week 13

1. Update `strategies/index.md` with the live result as its own row: the strategy, the window, live return, backtest return, gap.
2. Update `graveyard.md`: any rule or variant that died during the live window, including interventions.
3. Sketch the writeup's structure (you will write it properly next week): the question, the method, the three best artifacts, the three most instructive deaths, the honest limitation.

*Time: 3-4 h.*

### Sun — Phase retro, journal, gate

1. `reports/retro-P6.md` with the three questions.
2. `make gate WEEK=12`: 30+ equity rows, reconciliation with named components, post-mortem present, M5 confirmed.
3. Journal: what do you now believe about your backtest that you did not believe in Week 4?

*Time: 2-3 h.*

## Gate

`make gate WEEK=12` - see [gates/week-12-gate.md](gates/week-12-gate.md). **Milestone M5:** 30+ days of live logs, a reconciliation that attributes divergence to fees/slippage/timing/missed fills/regime, and a written expected-divergence budget for next month.

## Graveyard prompt

Any live rule you silently changed mid-run gets logged as a killed variant. Undisclosed mid-course edits are the most common way students cheat themselves - the market will not notice, but the reconciliation will, and your Week 13 writeup is supposed to be the honest one.

## Concept injections this week

- [C24 — Live vs Backtest Divergence](concepts/C24-live-vs-backtest-divergence.md) — triggered by live PnL 40% below backtest PnL with no obvious culprit
- [C25 — Regime Detection](concepts/C25-regime-detection.md) — triggered by discovering the whole divergence is one volatile month, not a bug
