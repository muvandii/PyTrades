# Signal generator spec (the live harness)

The live bot is a scheduled job with three responsibilities: **decide**, **record**, **report**.
It is deliberately boring. Anything clever in the harness is a risk, because a harness bug looks
exactly like a strategy loss.

## The daily cycle

```
 07:00  fetch/refresh bars for the universe        (data_fetcher, cached, validated)
 07:05  compute signals from the SPEC + latest bars (same code path as the backtest: generate())
 07:07  apply the Week 10 risk policy              (target vol, exposure cap, de-risking rule)
 07:10  diff target vs current positions -> orders (or explicit "no action" decisions)
 07:12  submit orders (broker adapter) or record paper fills
 07:15  write live/log/<date>.json: signals, targets, orders, fills, errors, equity
 07:20  rebuild live/dashboard.html               (from the JSON logs, no manual edits)
```

The timestamp is the bot's local schedule; the important property is that the *same code path*
that produced the backtest produces the live signal (`strategies/<id>/signal.py::generate`). A
re-implementation in the live bot is the most common source of unexplained divergence.

## Required artifacts per day

`live/log/YYYY-MM-DD.json`:

```json
{
  "date": "2026-11-03",
  "strategy": "S05_momentum",
  "spec_fingerprint": "…",
  "data": {"symbols": ["SPY", "QQQ"], "last_bar": "2026-11-02", "source": "stooq", "stale_days": 1},
  "signals": {"SPY": 1.0, "QQQ": 0.0},
  "targets": {"SPY": 0.33, "QQQ": 0.0},
  "positions_before": {"SPY": 0.33, "QQQ": 0.0},
  "orders": [{"symbol": "SPY", "side": "sell", "qty": 12, "type": "market", "reason": "rebalance"}],
  "fills": [{"symbol": "SPY", "qty": 12, "price": 512.44, "cost_bps": 3.1}],
  "equity": 101243.55,
  "skipped": [{"decision": "no_action", "reason": "target unchanged within 1% band"}],
  "errors": []
}
```

Rules:
- **Every decision is logged, including "do nothing".** A day with no orders still gets a file:
  silence is indistinguishable from a crashed bot.
- **`skipped` is not optional.** Each skip names the rule that caused it.
- **`errors` is a list, never a swallowed exception.** A fetch failure is logged, the bot
  continues, and the missing day is visible in the dashboard.
- The equity line each day goes into `live/equity.csv` (date, equity, cash, gross_exposure,
  positions_count, notes) - 30+ rows is the M5 requirement.

## Broker adapters

Two implementations ship with the course, both optional to *use* but both illustrating the shape:

1. **Paper adapter** (`live/broker_paper.py`): fills immediately at the last close plus a
   configurable slippage and cost; no network. Deterministic and reproducible - the default for
   the 30-day window if no API keys are available.
2. **Alpaca paper adapter** (`live/broker_alpaca.py`): real paper fills via `alpaca-py` with keys
   from environment variables only (never committed). Use it if you have keys; the reconciliation
   is more interesting with real fills, but the course does not require it.

Both adapters implement the same three methods: `positions()`, `submit(order)`, `fills(since)`.
Swapping adapters must not require touching the signal or policy code.

## Operational rules (each one exists because it has broken a student's run)

| Rule | Why |
| --- | --- |
| Run under a scheduler (cron/systemd/task scheduler), not by hand | unattended operation is the claim M5 grades |
| Idempotent per day: re-running must not duplicate orders | restart after a crash is the normal case |
| Guard against stale data: if the last bar is > 4 calendar days old, skip and log | trading on a stale signal is a silent look-ahead of one kind and a silent farce of another |
| Timezone: use the exchange's calendar, log UTC + local | a "missed" order is usually a timezone bug |
| Kill switch: `live/STOP` file stops new orders, never closes positions | you will want to stop the bot without creating a liquidation event |
| One process, one strategy | running two strategies in one process makes attribution impossible |

## What the harness must *not* do

- No re-implementation of the signal logic. Import it.
- No manual edits to positions outside the log ("I just fixed that one order") - if it happens,
  it is logged as a killed variant and the run restarts with an entry in `postmortem.md`.
- No strategy parameter changes during the window. The point of the window is to observe one
  fixed object; changing it mid-run means you have no observation at all.
