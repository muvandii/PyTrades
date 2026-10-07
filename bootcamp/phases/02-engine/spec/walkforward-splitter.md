# Walk-forward splitter specification (Week 4, D07)

## The rule

Parameters are chosen on data that ends **before** the period they are evaluated on.
That is the entire idea; everything else is bookkeeping.

```
|<----------- train ----------->|<- test ->|                        (rolling)
|<----------- train ----------->|<- test ->|
        |<----------- train ----------->|<- test ->|
```

## Interface

```python
splits(index, train_bars=756, test_bars=126, mode="rolling", embargo_bars=1) -> list[Split]
Split(train_start, train_end, test_start, test_end)     # ends are inclusive
```

- `rolling`: fixed-length train and test windows sliding forward.
- `expanding`: train window grows from the start; test windows still slide.
- `embargo_bars`: a gap between train end and test start. Use 1 bar by default; raise it to the
  signal's lookback when the signal is slow (a 200-day MA needs ~200 bars of warm-up, or the
  first test bars are computed on data the model was fit on).

Defaults for this course: 3 years train (756 bars), 6 months test (126 bars), 1 bar embargo.
Document any deviation in the report; deviation without a reason is the thing this course hunts.

## Required outputs

1. `reports/walkforward/<strategy>.csv`: one row per split with `train_start, train_end,
   test_start, test_end, chosen_params, is_sharpe, oos_sharpe, oos_return, oos_trades`.
2. A summary line in the tearsheet: mean OOS Sharpe, share of profitable splits, and the
   degradation ratio `mean OOS Sharpe ÷ mean IS Sharpe`.
3. A parameter-stability table: how often the "best" parameter changed between splits. If it
   changes every split, you are fitting noise; if it never changes, you are probably not
   optimising anything - either is a finding.

## Honesty rules

- The number you report is the **pooled out-of-sample result** (concatenate test windows), not
  the best split and not the average of IS and OOS.
- Every split you ran is reported, including the bad ones. A walk-forward that reports three
  good windows out of twelve is a failed walk-forward with a good press release.
- If you tune the walk-forward parameters (train length, thresholds) after seeing the results,
  say so and treat the whole exercise as in-sample. That is not a failure; hiding it is.
