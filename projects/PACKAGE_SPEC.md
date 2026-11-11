# `pytrades/` Package Specification & Evolution (Days 10–13)

> **Why `pytrades/` is not pre-created for you:** graduating from scattered notebook
> cells to an importable Python package is the core engineering lesson of Days 10–12.
> Create `pytrades/` at the repository root (`/path/to/PyTrades/pytrades/`) from your
> own tested Week 1–2 implementations.

## Target layout

```text
PyTrades/
└── pytrades/
    ├── __init__.py      # exposes __version__ ("0.1.0" Day 10 -> "0.2.0" Day 11 -> "0.3.0" Day 12)
    ├── data.py          # Day 01-02 intake/slicing + Day 12 vendor/API adapters
    ├── indicators.py    # Day 06 returns & moving averages (+ Day 13 capstone helpers if needed)
    └── strategy.py      # Day 08-10 backtest functions + Day 11 strategy classes
```

## Module inventory (harvested from Milestones 1–3)

### `pytrades/data.py`
| Version | Function | Contract source |
|---|---|---|
| v0.1 (Day 10) | `validate_ohlcv(df)` | Day 01 Ex 3 — returns `True` or raises descriptive `ValueError` (empty, non-DatetimeIndex, unsorted, duplicate dates, missing OHLCV, non-positive price, negative volume) |
| v0.1 (Day 10) | `load_prices(csv_path)` | Day 02 — loads CSV with `DatetimeIndex`, sorted ascending, validated |
| v0.1 (Day 10) | `slice_prices(obj, start, end)` | Day 02 — inclusive date slice; empty result or `start > end` raises `ValueError` |
| v0.3 (Day 12) | `parse_av_daily(payload)` | Day 12 Ex 1 — parses Alpha-Vantage-style JSON dict into a validated OHLCV `DataFrame` |
| v0.3 (Day 12) | `normalise_vendor_columns(df, mapping)` | Day 12 Ex 2 — renames required vendor columns, drops extras, raises `ValueError` on missing required fields |
| v0.3 (Day 12) | `fetch_daily(symbol, api_key=None, _get=None)` | Day 12 Ex 4 — reads key from argument or `ALPHAVANTAGE_API_KEY` env var (never hard-coded), uses injectable `_get` transport for offline testing |

### `pytrades/indicators.py`
| Version | Function | Contract source |
|---|---|---|
| v0.1 (Day 10) | `simple_returns(prices)` | Day 06 Ex 1 — `pct_change`, first row `NaN`, input unmodified |
| v0.1 (Day 10) | `log_returns(prices)` | Day 06 Ex 1 — `ln(P_t / P_{t-1})`, any `<= 0` price raises `ValueError` |
| v0.1 (Day 10) | `sma(prices, window)` | Day 06 Ex 2 — `rolling(window, min_periods=window).mean()`, int `window >= 1` (reject `bool`) |
| v0.1 (Day 10) | `ema(prices, span)` | Day 06 Ex 3 — `ewm(span=span, min_periods=span).mean()`, int `span >= 1` (reject `bool`) |

### `pytrades/strategy.py`
| Version | Object | Contract source |
|---|---|---|
| v0.1 (Day 10) | `positions_from_signal(signal)` | Day 08 Ex 3 — `{-1, 0, 1}` (`NaN -> 0`), `.shift(1, fill_value=0)`, `int` dtype, `name="position"` |
| v0.1 (Day 10) | `long_only_positions(signal)` | Day 09 Ex 1 — maps `-1 -> 0`, `.shift(1, fill_value=0)`, `int` dtype, `name="position"` |
| v0.1 (Day 10) | `apply_transaction_costs(strategy_log_returns, positions, cost_rate=0.001)` | Day 09 Ex 2 — deducts `cost_rate * |Δposition|` with initial cash `0` |
| v0.1 (Day 10) | `performance_summary(log_returns, periods_per_year=252)` | Day 08 Ex 4 — `total_return`, `annualised_vol`, `max_drawdown` (`$1.00` peak anchor), `n_days` |
| v0.1 (Day 10) | `trade_count(positions)` | Day 08 Ex 5 — count of bars where `position != prev_position` (prior cash `0`) |
| v0.1 (Day 10) | `test_strategy(prices, fast=50, slow=100, long_only=True, cost_rate=0.0)` | Day 10 Ex 1 — pure data-in/dict-out summary on `prices.index[slow:]` |
| v0.2 (Day 11) | `SMACrossoverStrategy` | Day 11 Ex 4 — validated state, cached `.run()`, cache-invalidating setters/`set_parameters`, `.summary()`, `.plot()` |
| v0.2 (Day 11) | `EMACrossoverStrategy` | Day 11 Ex 5 (Challenge 4) — EMA crossover reusing the base strategy lifecycle |

## Engineering non-negotiables across all versions

1. **Zero notebook globals:** no module may reference `df`, `df_long`, `close_panel`, or file paths at import time.
2. **No caller mutation:** inputs passed into functions or `__init__` are never modified in place.
3. **No silent failures:** invalid windows, non-positive prices, rate-limit payloads, and pre-`.run()` `.summary()` calls raise explicit exceptions (`ValueError` / `RuntimeError`).
4. **No hard-coded secrets:** API keys are never written in source files or notebooks.

## Changelog checkpoints (record in your commit messages)

- **v0.1.0 (Day 10 — P2.2):** initial extraction of `data.py`, `indicators.py`, `strategy.py` functions; verified via clean-namespace import in Day 10 Section F/G.
- **v0.2.0 (Day 11 — P2.3):** added `SMACrossoverStrategy` and `EMACrossoverStrategy` delegating maths to v0.1 functions; verified parity `class.summary() == test_strategy(...)`.
- **v0.3.0 (Day 12 — P2.4):** added offline-testable vendor adapters (`parse_av_daily`, `normalise_vendor_columns`, `fetch_daily`) to `data.py`; end-to-end canned-JSON → backtest run green.
