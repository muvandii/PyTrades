# Testing guide: what "tested" means in this course

Three kinds of tests, in order of how often they save you.

## 1. Oracle tests (what is my number supposed to be?)

Hand-compute a tiny case, assert your function matches it. `kit/tests/test_metrics.py`
is 25 of these, and it is the oracle your `engine/metrics.py` is judged against from Week 3.

```python
def test_max_drawdown_is_peak_to_trough():
    equity = pd.Series([1.0, 1.2, 0.6, 1.3])
    assert metrics.max_drawdown(equity) == pytest.approx(-0.5)
```

Rule: if you cannot compute the expected value on paper, you are testing nothing.

## 2. Contract tests (does my engine behave like the reference?)

`kit/tests/test_spine_contract.py` runs twice in this course: once against
`kit.spine` (reference), once against YOUR engine:

```bash
PYTRADES_ENGINE=engine.backtest python -m pytest kit/tests/test_spine_contract.py -q
```

It pins what makes a backtest honest: signals execute one bar later, constant weight
replicates buy-and-hold, costs scale with turnover, look-ahead shows up as a measurable
premium, saved results reload identically.

## 3. Adversarial tests (where does this die?)

Not unit tests: experiments. Every one belongs in a report, not in `tests/`.

| Question | How to answer it |
| --- | --- |
| Does it survive 2x costs? | `make costs S=<id>`, read the 10-20 bps rows |
| Is it a spike or a plateau? | sweep the parameter, plot the surface, inspect neighbours |
| Is the edge one trade? | share of total PnL from the largest trade |
| Is it one period? | yearly Sharpe table; drop the best year and re-check |
| Is it luck? | block bootstrap CI on the OOS Sharpe |
| Would random entries do as well? | same holding period, random entries, 500 runs |

## What does NOT count as testing

- Running it once and liking the result
- A DataFrame with 2,000 rows and 3 trades
- A test with no assertion (a print is not a test)
- A test on synthetic data used to judge a market claim
