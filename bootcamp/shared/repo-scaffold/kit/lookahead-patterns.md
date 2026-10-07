# Look-ahead bias: the catalogue

Every entry is a real bug that has eaten a real backtest. Check them in order - the
first three account for most of the damage.

## A. Time axis

| # | Pattern | Example | Fix |
| --- | --- | --- | --- |
| A1 | share-bar execution | `pnl = signal * returns` (same bar) | `signal.shift(1)` or next-open fills |
| A2 | same-bar close fill | decide at close[t], fill at close[t] | fill at open[t+1] (or close[t+1]) |
| A3 | full-sample statistics | `(p - p.mean()) / p.std()` | rolling/expanding stats, or train-only fitting |
| A4 | backward fill | `df.bfill()` on any input feature | `ffill()` only, with a documented expectation |
| A5 | rebalancing on a future-known schedule | "rebalance on the last day of the month" computed with a full-month period | use period-to-date masks only |
| A6 | survivorship universe | today's tickers backtested over 15 years | point-in-time universe |
| A7 | restated fundamentals | current EPS series used historically | as-reported data with publication dates |
| A8 | split/dividend leakage | raw prices where adjusted are needed | consistent adjustment, documented |

## B. Selection axis (equally fatal, harder to see)

| # | Pattern | Example | Fix |
| --- | --- | --- | --- |
| B1 | parameter sweep reported at the max | best of 1,600 pairs | hold out, or report the whole surface |
| B2 | strategy chosen after seeing results | "I tested 12 ideas, here is the one that worked" | disclose and deflate: count the trials |
| B3 | pair/symbol chosen on the full sample | cointegration test over all data | select on train, test on holdout |
| B4 | threshold tuned on the OOS window | z-score 2.0 picked after peeking | freeze parameters before OOS |
| B5 | data snooping across the whole pipeline | cleaning that removed exactly the bad trades | log every cleaning decision with its date |

## C. Engine-level bugs

| # | Pattern | Example | Fix |
| --- | --- | --- | --- |
| C1 | using the trade bar's open with a decision made at its close | positions[t] from signals[t] | shift once, always |
| C2 | costs applied after PnL comparison | optimising gross, reporting net | costs in the engine, not in the report |
| C3 | partial fills assumed complete | filling 100% at the close price | model slippage proportional to turnover |
| C4 | timezone/day-boundary errors | daily bars stamped 00:00 UTC used as local | normalise to naive local dates |
| C5 | look-ahead via pandas alignment | assigning a Series with a different index | assert `.index.equals()` before arithmetic |

## How to prove you are clean

1. `signal_shift=0` vs `signal_shift=1`: the difference is your look-ahead premium. If
   shift-0 is dramatically better, you have an A1/A2 problem somewhere in the signal.
2. Time-travel test (Week 3 deliverable): re-run the engine on data truncated at date T
   and compare positions up to T against the full-sample run. They must be identical.
3. Fresh-data test: run the same spec on a symbol you have never looked at. If the
   behaviour changes character completely, you were fitting something.
