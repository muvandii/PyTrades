# M5 — Live paper (end of Week 12)

## Pass condition

> 30 days of live paper logs plus a reconciliation report; live vs backtest divergence explained.

Verbatim from the course registry. The 30-day clock starts in **Week 5** (create
`live/config.json` then); the harness that trades it is built in Week 11; M5 is confirmed at the
Week 12 gate (manual check G12.6).

## What it proves

That your strategy, your risk policy and your operational discipline survive contact with a live
clock: real calendar dates, real data arrivals, real acknowledgements, and a real, measurable gap
between what the backtest promised and what the account did. This is the milestone that separates
"backtester" from "practitioner" - and it is the one that no amount of backtesting can substitute
for.

## Supporting requirements

- 30+ rows in `live/equity.csv`, one per trading day, no unaccounted gaps
- One JSON log per day (including no-trade days) with signals, targets, orders, fills, equity, skipped, errors
- A shadow backtest re-run as of each live day, spot-checked against at least ten logged decisions
- `live/reconciliation.md` attributing divergence to fees, slippage, timing, missed fills, sizing, regime - with the components summing to the total
- `live/postmortem.md` with failures, interventions (as killed variants), and an expected-divergence budget
- The traded strategy unchanged through the window (spec fingerprint matches)

## Fail path

| Symptom | Diagnosis | Fix |
| --- | --- | --- |
| fewer than 30 days | clock started in Week 11 | keep running into Week 13; label the writeup "M5 in progress"; do not backfill rows |
| log gaps | unattended execution was not unattended | add a watchdog/alert that answers "did the bot run today?" and log skipped days explicitly |
| unexplained bucket > 10% | not enough investigation, or genuinely missing data | work Tuesday's list; if it stays high, publish it as a finding with what data would close it |
| live beats the backtest | often a sizing difference, not skill | decompose before celebrating; a smaller position in a bad window looks like alpha |
| mid-run manual edits | the run is no longer a policy test | log as killed variants; restart the window for the policy claim |
| the strategy was changed | the observation is void | restart with the fingerprint frozen and say so in the writeup |

## Remediate before Week 13

The capstone writeup quotes the reconciliation, so before you start writing: confirm every number
in it traces to a log file or a shadow-backtest artifact, and that the divergence budget is a
sentence you would defend in public. If M5 is still in progress, that is a legitimate Week 13
state - the writeup simply says "live paper window: 24 of 30 days, reconciliation preliminary",
which is more valuable than a fabricated 30.
