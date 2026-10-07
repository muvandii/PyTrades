---
week: 11
phase: P6
title: Go Live (Paper)
deliverables: [D16]
concepts: [C23]
milestone: null
hours: 14-18
---

# Week 11 — Go Live (Paper)

## Learning objective

Ship a scheduled bot that trades your Week 10 risk policy - not your mood - and keep it running unattended for seven consecutive days while producing a daily log a stranger could audit.

## Deliverable

- [D16 — Live harness running](deliverables/D16.md): `live/bot.py`, `live/broker_paper.py` (or Alpaca), daily logs, `live/dashboard.html`.

## Daily tasks

### Mon — Wire the harness

1. Build `live/bot.py` to the schedule in [spec/signal-generator-spec.md](spec/signal-generator-spec.md): refresh data → existing `generate()` signal → risk policy → diff → orders → log → dashboard.
2. Use the paper adapter first (`live/broker_paper.py`: immediate fills at last close ± your assumed slippage). Deterministic, no keys, no excuses.
3. Critical implementation property: the signal comes from the **same code path** as the backtest. Import `generate()`; do not re-implement it.

*Time: 3-4 h.*

### Tue — Harden it before trusting it

1. Idempotency: running the bot twice on the same day must not duplicate orders. Write the guard and test it by running twice.
2. Stale-data guard: if the last bar is more than 4 calendar days old, skip and log. Test it by pointing the bot at a truncated data file.
3. Kill switch: a `live/STOP` file stops new orders without closing positions. Test it.
4. Inject [C23 — Slippage Modeling & Latency](concepts/C23-slippage-modeling-and-latency.md): the paper adapter's fill is an assumption, and today you write down exactly what it assumes.

*Time: 4-5 h.*

### Wed — Start the unattended run

1. Schedule the job (cron, systemd timer, Task Scheduler, or a long-running loop with a sleep - any of these counts if it runs without you).
2. Verify the first day's log against the spec: signals, targets, orders, fills, equity, skipped decisions, errors. All six fields present.
3. Write `live/README.md`: which broker adapter, which schedule, how to read a log day, how to stop the bot.

*Time: 3-4 h. From here the bot must run for at least 7 consecutive days - but your 30-day window started in Week 5, so the clock is already ahead of you.*

### Thu — Dashboard from the logs

1. `live/dashboard.html`, generated *from* `live/log/*.json` by a script (never edited by hand): current positions, equity curve, today's decisions, error count, days logged, and a backtest-vs-live overlay over the live window.
2. Add one panel that answers "did the bot run today?" - the single most useful live panel in existence.

*Time: 3-4 h.*

### Fri — Watch it fail, in a controlled way

Deliberately break things and confirm the log tells you:

1. Truncate the data file and re-run: does the stale-data guard fire and log?
2. Feed a universe with a missing symbol: does it fail loudly, or silently trade a partial book?
3. Kill the process mid-run: does the next run pick up idempotently?

Record which failure modes produced a *silent* success. Those are the ones that will show up in
Week 12's reconciliation as unexplained divergence.

*Time: 3-4 h.*

### Sat — Live vs backtest, first look

1. Re-run the backtest over the live window with the same costs and the same spec fingerprint. Compare against the live log day by day.
2. Write the first version of `live/reconciliation.md` using `shared/templates/reconciliation.md`: the gap table by component (costs, slippage, timing, missed fills, sizing).
3. Anything you cannot attribute today goes into an "unknown" row with an investigation note - not into a footnote.

*Time: 3-4 h.*

### Sun — Journal, gate

1. `make gate WEEK=11`: `live/bot.py` exists, 7+ daily logs, `live/dashboard.html` exists. At this point the run should also have ~6 weeks of history from the Week 5 clock start.
2. Journal: what did running unattended change about your confidence in the strategy? (Usually it drops, and for good reasons.)

*Time: 2-3 h.*

## Gate

`make gate WEEK=11` - see [gates/week-11-gate.md](gates/week-11-gate.md). **Checkpoint:** the bot runs unattended for 7 consecutive days - signals generated, orders submitted or explicitly skipped, every day logged, dashboard rebuilt - and it has been running longer than that, because you started the clock in Week 5.

## Graveyard prompt

Log every operational death: missed bar, stale data, broker timeout, double order, timezone bug, duplicate process. Ops bugs are the leading cause of strategy death in the real world, and each one belongs in the graveyard with the same rigor as a `cost death`.

## Concept injections this week

- [C23 — Slippage Modeling & Latency](concepts/C23-slippage-modeling-and-latency.md) — triggered by live fills being systematically worse than the close your backtest assumed
