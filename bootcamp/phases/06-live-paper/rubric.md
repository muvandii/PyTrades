# Phase 6 rubric — Live paper (Weeks 11-12)

| Criterion | 0 (not yet) | 1 (passing) | 2 (strong) | If you scored low |
| --- | --- | --- | --- | --- |
| **Unattended operation** | run by hand, gaps unexplained | 7+ consecutive days scheduled, gaps logged | 30 days with zero unlogged days and a watchdog that reports "did the bot run?" | add the watchdog before adding anything else |
| **Log completeness** | orders only | signals, targets, orders, fills, equity per day | skipped decisions and errors logged with reasons | log the no-trade days; silence is indistinguishable from a crash |
| **Idempotency** | untested | double-run produces no duplicate orders | crash-recovery tested mid-run | run the bot twice, then kill it mid-run and restart |
| **Data hygiene** | traded on stale bars | staleness guard implemented and tested | data source, last-bar date and staleness logged daily | point the bot at a truncated file and confirm the guard fires |
| **Same-code-path** | signal re-implemented in the bot | `generate()` imported from the strategy | a fingerprint check in the log proves it | grep `live/` for signal logic; there should be none |
| **Reconciliation** | prose | component table with numbers | components sum within rounding, unexplained < 10% | work the list in `week-12.md`; nothing else moves the verdict |
| **Post-mortem honesty** | missing | failures and interventions listed | interventions logged as killed variants + expected-divergence budget | write the budget sentence: X bps/month, Y structural |
| **Regime awareness** | blame the market | window vol vs backtest median computed | historical analogues used to predict the window's expected divergence | compute vol20 for both and compare distributions |

## Phase 6 retro

Write `reports/retro-P6.md`: the pattern that killed rules and runs (usually operations), the
concept that changed your live process most (usually C23 - measuring rather than assuming
slippage), and the thing you are still fooling yourself about (usually "my backtest is
conservative", which the reconciliation just disproved or confirmed).

## Pass bar

- M5 passed, or in progress with an honest statement and a preliminary reconciliation
- 30+ equity rows (or the true count, stated), one log per day including no-trade days
- Reconciliation components sum to the observed gap within rounding
- Post-mortem contains the expected-divergence budget for the next month
- Every intervention during the window is logged as a killed variant in the graveyard
