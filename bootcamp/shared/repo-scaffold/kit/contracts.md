# The four contracts (frozen - your whole portfolio depends on them)

Anything in this course that produces or consumes a result does it through these
four shapes. They are frozen for 13 weeks on purpose: if you change one, every
earlier verdict becomes irreproducible.

## 1. DATA

```
data/<SYMBOL>.csv          # columns: date,open,high,low,close,volume
data/<SYMBOL>.meta.json    # provider, fetched_at, rows, first, last, sha256, synthetic
```

Rules: never hand-edit a CSV (re-fetch it, or write the problem down). Synthetic data
never supports a verdict. `kit/data_fetcher.py` is the only writer.

## 2. SPEC

```
config/<strategy_id>.json -> kit.spine.StrategySpec
```

```json
{
  "id": "S01_ma_cross",
  "name": "MA cross 50/200 on SPY",
  "universe": ["SPY"],
  "params": {"fast": 50, "slow": 200},
  "thesis": "one sentence, from templates/thesis.md",
  "tags": ["trend", "tier2"],
  "long_only": true,
  "signal_file": "signal.py",
  "max_gross_exposure": 1.0,
  "rebalance": "daily"
}
```

The spec is your experimental record: id, universe, parameters, thesis, constraints.
`spec_fingerprint` (spec + signal code) goes into every result's `meta.json`.

## 3. SIGNAL

```
strategies/<id>/signal.py

def generate(prices: dict[str, DataFrame], params: dict) -> DataFrame:
    """Target weights in [-1, 1], one column per symbol, index = decision bars.
    Deciding at bar t is fine. Executing at bar t is the engine's job (t+1)."""
```

Hard rules the engine enforces: no NaN-only frames, no |weight| > `max_gross_exposure`,
no shorts when `long_only` is true. Signals are **targets**, not trades: the engine
handles shifting, sizing clips, turnover and fills.

## 4. RESULT

```
reports/backtests/<name>/
├── equity.csv      # date,equity
├── positions.csv   # date,<SYMBOL>... (executed target weights)
├── trades.csv      # symbol,side,entry_time,exit_time,bars_held,avg_weight,return,pnl,cost
├── metrics.json    # every metric, machine-readable
└── meta.json       # name, spec+data fingerprints, costs, execution, bars, turnover
```

Rules: a result without `meta.json` cannot appear in a verdict, because you cannot
prove which spec, data or costs produced it. `BacktestResult.load(name)` must work for
every saved artifact, forever - that is what makes Week 12's reconciliation possible.

## Compatibility checklist for your engine (Week 4 gate)

```python
from engine.backtest import run_backtest, StrategySpec, BacktestResult
run_backtest(spec, name=None, prices=None, signals=None, start=None, end=None,
             initial_capital=100_000, fee_bps=0.0, slippage_bps=0.0,
             execution="next_open", data_dir="data", signal_shift=1)
```

`BacktestResult` exposes `.equity .returns .positions .trades .metrics .meta`,
`.state_at(ts)`, `.save()`, `.load()`. Prove it: `make test-contract`.
