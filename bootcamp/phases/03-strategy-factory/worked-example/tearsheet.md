# Tearsheet — S03_worked (Bollinger z-score reversion, tight threshold)

**Data:** `data/LAB_MR.csv` (laboratory series, synthetic) · **Bars:** 2,600 (2010-01-01 → 2019-12-19) · **Cost assumption:** 5 bps fee + 5 bps slippage per side unless stated

> ⚠️ Laboratory data. This tearsheet demonstrates the *method*, not a market result. Verdicts
> built on lab data must say "not market evidence".

## Headline

| Metric | Gross (0 bps) | Net (20 bps round trip) |
| --- | --- | --- |
| CAGR | +6.15% | **−1.67%** |
| Sharpe | 0.47 | **−0.04** |
| Max drawdown | −33.0% (1,104 bars long, never recovered in sample) | **−54.4%** (2,084 bars, never recovered) |
| Ulcer index | 14.6% | 28.6% |
| Calmar | 0.19 | −0.03 |
| Turnover | 38.2×/yr — identical in both columns (costs do not change the signal) | |
| Trades / win rate / profit factor | 197 / 59.4% / 1.26 | 197 / 52.3% / 0.94 |

## Out-of-sample (sample split at 2014-12-26, net of 20 bps)

| Window | Bars | CAGR | Sharpe | Max DD | Total return |
| --- | --- | --- | --- | --- | --- |
| IS (2010-01 → 2014-12) | 1,301 | +3.24% | +0.28 | −27.0% | +17.9% |
| OOS (2014-12 → 2019-12) | 1,300 | −6.34% | **−0.37** | −47.3% | −28.7% |

The in-sample result was already mediocre; the out-of-sample half is outright negative. Costs
are not the only problem — but they are the part you could have measured before running anything.

## Cost sweep

| Round-trip bps | CAGR | Sharpe |
| --- | --- | --- |
| 0 | +6.15% | 0.47 |
| 4 | +4.54% | 0.37 |
| 8 | +2.95% | 0.27 |
| 12 | +1.39% | 0.17 |
| 16 | −0.15% | +0.07 |
| 20 | −1.67% | −0.04 |
| 30 | −5.36% | −0.29 |
| 40 | −8.92% | −0.54 |

**Breakeven: ≈ 15.7 bps round trip.** Above that, this strategy loses money with certainty.

## Trade anatomy (gross run)

- 197 trades, mean holding 5.3 bars (median 4) — the turnover is structural, not incidental.
- Mean win +2.10%, mean loss −2.21%, payoff ratio 0.95: the edge is a *win-rate* edge at 59.4%
  (this is the family where win rate and edge happen to point the same way — see C03 for the case
  where they do not).
- The largest 5% of trades produce 95% of gross PnL. That is not a healthy distribution: it says
  the gross edge is carried by a handful of episodes, and a slightly different exit rule would
  have missed them.

## Fragility

| Test | Result | Reading |
| --- | --- | --- |
| Window sweep (net 20 bps) | 4→−0.05, 5→−0.04, 6→+0.04, 8→+0.22, 10→+0.27 | **not a cliff**: patience buys survival. The death is caused by turnover, and the turnover column predicted it |
| Entry threshold (net 20 bps) | −0.8→−0.05, −1.0→−0.04, −1.2→+0.23, −1.5→+0.33, −2.0→0.00 (too few trades to matter) | same story: the tighter the trigger, the more spread you pay |
| 2× cost assumption (40 bps) | CAGR −8.9% | hopeless, not marginal |
| Drop best year | net CAGR falls from −1.7% to −7.7% | there was no "good year" to remove — the strategy never had one net |
| Bootstrap 95% CI on OOS Sharpe | **[−1.21, +0.44]** | includes zero, and straddles it widely |

## What this does not tell you

That the reversion family is worthless. It tells you that **this specification at 38×/yr turnover**
is worthless at realistic spreads, and it shows the mechanism: a 5-day window with a −1.0σ trigger
trades every few days and pays 15.7 bps of edge to the spread. The loose variant of the same
signal (`window=20`, `entry_z=−2.0`, 8.3×/yr) survives the whole sweep on the same data. Nothing
here speaks to whether the underlying reversion tendency is real; only to whether a signal that
trades this often can pay for itself.
