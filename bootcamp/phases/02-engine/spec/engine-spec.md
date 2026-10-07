# Engine specification (Weeks 3-4) — what to build, and what "correct" means

You are replacing `kit/spine.py` with your own `engine/`. The kit stays as the oracle:
same inputs, same outputs, same files. Nothing in the course changes shape.

## Scope

| In scope | Out of scope (explicitly) |
| --- | --- |
| daily bars, equities/ETFs/crypto | intraday, order-book simulation |
| market orders filled at next open/close | limit orders, partial fills by size |
| turnover-based costs | borrow costs, financing, taxes, margin rules |
| long or long/short weights, gross ≤ max | options, futures rolls, shorting constraints per name |
| one account, one currency | multi-currency, corporate actions beyond provided prices |

Out-of-scope items are not "later": they are decisions you make once and write down in
`engine/README.md` so your verdicts carry their limits.

## Module layout

```
engine/
├── __init__.py
├── data.py         # DATA contract: load prices, validate presence, return dict[str, DataFrame]
├── events.py       # the order/fill/position event loop (accounting)
├── backtest.py     # run_backtest + BacktestResult  (the contract surface)
├── costs.py        # turnover-based cost model, unit-tested
├── metrics.py      # your rebuild of kit/metrics.py (validated against the oracle tests)
├── walkforward.py  # Week 4: splits, OOS runner, parameter sweeps
├── tearsheet.py    # Week 4: markdown tearsheet generator
└── README.md       # what exists, what changed, what it broke, what is out of scope
```

## The contract surface (must match exactly)

```python
run_backtest(
    spec, name=None, prices=None, signals=None, start=None, end=None,
    initial_capital=100_000, fee_bps=0.0, slippage_bps=0.0,
    execution="next_open", data_dir="data", signal_shift=1,
) -> BacktestResult

BacktestResult: .equity .returns .positions .trades .metrics .meta
                .state_at(ts) -> {"timestamp", "equity", "positions"}
                .save(directory=None, results_dir="reports/backtests") -> str
                .load(name_or_path, results_dir=...) -> BacktestResult  (classmethod)
```

`StrategySpec` stays the dataclass from the kit: `id, name, universe, params, thesis,
tags, long_only, signal_file, max_gross_exposure, rebalance`, with
`.fingerprint()` hashing spec **and signal file contents**.

## Behavioural requirements (numbered, testable)

1. **Execution lag.** `signal[t]` is a target decided with data up to bar `t`. The position
   carried through bar `t` is `signal[t-1]`. `signal_shift=0` exists only as a deliberate
   look-ahead demonstration and must never be used in a reported result.
2. **Next-open semantics.** With `execution="next_open"`, bar `t`'s portfolio return splits:
   overnight applies to the position held *into* the bar, intraday to the position set by
   the fill. You cannot capture the gap on the bar you decided, ever. With
   `execution="next_close"`, the position is marked at the close it was filled at.
3. **Exposure cap.** Target weights are scaled down until gross exposure ≤
   `max_gross_exposure`. Scale, never truncate silently.
4. **Costs.** `cost[t] = Σ|weight[t] − weight[t−1]| × (fee_bps + slippage_bps) / 10_000`,
   charged as a cash deduction in the loop, included in `trades.csv` per trade (entry+exit legs).
5. **Accounting.** Equity = cash + Σ(quantity × price). Positions are quantities, not weights;
   weights are targets. The two diverge between rebalances - that drift is real.
6. **Provenance.** `meta.json` includes `spec_fingerprint`, `data_fingerprint`, `created_at`,
   `execution`, `signal_shift`, `fee_bps`, `slippage_bps`, `bars`, `first_bar`, `last_bar`,
   `turnover_annual`, `total_cost_drag`. A result without provenance cannot appear in a verdict.
7. **Persistence.** `save()`/`load()` round-trip: metrics identical to floating-point tolerance,
   trades identical in count and total PnL.
8. **Validation, loudly.** Reject: all-NaN signals, `|weight| > max_gross_exposure` after scaling,
   shorts when `long_only` is true, infs, signals missing a universe column. Fail with a message
   that names the file and the column.

## Performance envelope

Not a speed contest, but it must stay usable: a 10-symbol daily backtest over 20 years
(~5,000 bars) should complete in a few seconds. If it takes minutes, you are looping over
DataFrame cells; vectorise the return series while keeping the accounting explicit.

## The three proofs (Week 3-4 gate)

1. **Buy-and-hold identity.** Constant weight 1.0 with `execution="next_close"` on SPY
   reproduces the price ratio within 1%.
2. **Time travel.** Re-running on data truncated at T produces identical positions and
   equity up to T as the full-sample run.
3. **Contract suite.** `PYTRADES_ENGINE=engine.backtest python -m pytest kit/tests/test_spine_contract.py -q`
   passes unchanged.

## Anti-goals

- Do not add features to make a strategy look better. Every feature is a decision that must
  be justified in `engine/README.md`.
- Do not "improve" the cost model during a week in which you are evaluating strategies.
  Costs are part of the experiment; changing them mid-experiment invalidates comparisons.
- Do not delete the kit. It is the reference you will be compared against in Week 12.
