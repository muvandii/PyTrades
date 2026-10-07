# Recall test — the course's exit exam (10-15 minutes of honesty)

No notes, no repo, no searching. Answer out loud or in writing, then check yourself.
**Pass standard:** three concepts explained correctly, one coded from scratch in an empty file.
This is diagnostic, not punitive: every gap you find here is one you would otherwise find in a
drawdown.

## Part 1 — Explain, from memory (pick three)

For each: the formula, why it matters, and one way to get it wrong.

| # | Concept | You must include |
| --- | --- | --- |
| 1 | Annualisation | scaling of means vs deviations (√), frequency inference |
| 2 | Expectancy & profit factor | formula, and when profit factor lies |
| 3 | Why win rate ≠ edge | an example with a high win rate and negative expectancy |
| 4 | Max drawdown & recovery | peak-to-trough, duration, time-to-recovery; why Sharpe can look fine |
| 5 | Sharpe ratio | what it normalises, what it ignores (path, tails, autocorrelation) |
| 6 | Bootstrap CI for Sharpe | block length and why; what the interval does *not* cover |
| 7 | Parameter plateaus | plateau vs spike, plateau width in parameter units |
| 8 | Overfitting deflation | best-of-N inflation ~ `√(2 ln N)/√years` |
| 9 | Cointegration & half-life | the test, the half-life formula, and why a long half-life kills the trade |
| 10 | Vol targeting | causal σ, cap, and why Sharpe can rise without predicting returns |
| 11 | Kelly & fractional Kelly | f* = μ/σ², growth-vs-fraction relation, why estimation error argues for a fraction |
| 12 | Risk of ruin | why it is a property of rules + strategy, not of the strategy |
| 13 | Slippage & latency | spread + impact + timing drift; why slippage is asymmetric |
| 14 | Live/backtest divergence | the component identity and sign conventions |
| 15 | Regime splits | causal state variable; why a short window needs a regime benchmark |

## Part 2 — Code, from scratch (pick one)

In an empty file, no imports from your repo (numpy/pandas allowed):

1. `max_drawdown(equity)` plus `drawdown_duration(equity)` - peak-to-trough and the longest run below a peak.
2. `sharpe(returns, rf=0.0)` handling frequency inference and zero-variance data.
3. Block bootstrap 95% CI for Sharpe of a return series.
4. `cost_sweep(prices, signal_fn, bps_grid)` returning CAGR/Sharpe per level and the breakeven bps.
5. A causal volatility target: `w = (target / (std(r, 60) * sqrt(252))).clip(0, 3)` applied with a one-bar shift.
6. Cointegration pipeline: hedge ratio by OLS, ADF p-value, half-life from the AR(1) coefficient.

**Standard:** the code runs, produces a plausible number, and you can say what would make it wrong.
The rubric: correct (2 points), edge cases handled (1), you can spot a broken variant (1). Six is
a pass.

## Part 3 — Spot it wrong (spend 5 minutes)

Open `tools/spot_it_wrong.py` (19 snippets) and explain, for five of them, what the bug is and what
it would do to a verdict. No running the file first; running it is the answer key.

## Part 4 — Two sentences (write these in your journal)

1. The concept you explained most shakily, and the one-sentence reason why.
2. The concept you now trust most about your *own* process - and the artifact that earned that trust.
