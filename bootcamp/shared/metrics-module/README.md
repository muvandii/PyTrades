# Module: metrics

**Canonical code:** `../repo-scaffold/kit/metrics.py` (ships as `kit/metrics.py`)
**Oracle tests:** `../repo-scaffold/kit/tests/test_metrics.py` (25 hand-computed cases)
**Used in:** Week 1 (D02), then rebuilt by you in Weeks 3-4
**Student artifact:** `engine/metrics.py` + `tests/test_metrics.py` that matches the oracle

## Why you rebuild something that already exists

Because "I can explain every metric I use" is a course outcome, and the fastest way to
earn it is to write `sharpe()` and then watch your version disagree with the oracle by
a factor of `sqrt(252)`. You will not forget that mistake.

## The order you will meet them

| Week | Metric | Triggering failure |
| --- | --- | --- |
| 1 | total return, CAGR, compounding | first equity curve |
| 1 | expectancy, win rate, profit factor | first "90% win rate" claim |
| 3 | vol, Sharpe, Sortino | comparing two strategies |
| 4 | max drawdown, duration, Calmar, Ulcer | seeing a 47% drawdown |
| 5 | bootstrap CI of Sharpe | two survivors 0.3 apart |
| 6 | t-stat of mean return | "is this distinguishable from zero?" |
| 10 | portfolio variance, correlation | combining legs |

## Interface you must reproduce

```python
metrics.sharpe(returns, rf=0.0, index=None, ppy=None) -> float
metrics.max_drawdown(equity) -> float            # negative number by convention
metrics.trade_stats(trades) -> dict              # expectancy, profit factor, ...
metrics.summary(result_or_equity, trades=None) -> dict
metrics.tearsheet(metrics_dict, title="...") -> str   # markdown
```

## Conventions that prevent nonsense

- Returns are simple (arithmetic), not log, unless a function says otherwise.
- Drawdowns are negative percentages.
- `periods_per_year` is INFERRED from the index, or passed explicitly - never assumed
  silently. A monthly strategy annualised as daily is wrong by 4.6x.
- Metrics never adjust for costs. Costs are the engine's job. A metric that quietly
  fixes your PnL is a metric that hides your bugs.
