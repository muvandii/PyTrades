# Cost model specification (Week 3, D06)

## The model

```
turnover[t]  = Σ_symbols | target_weight[t] − target_weight[t−1] |
cost_cash[t] = turnover[t] × (fee_bps + slippage_bps) / 10_000 × equity[t−1]
```

Charged in the loop, before compounding the bar's return. Round-trip bps in course tables
means fee + slippage already summed per side (so "10 bps" is about 5 bps each way).

## Why turnover and not trade count

A trade count hides size and netting. If two symbols move in opposite directions and you count
one "rebalance", you charged one trade for two notional sides. Turnover measures the notional
that actually crossed the spread:

| Strategy | Trades/month | Turnover/month | Implied cost at 10 bps |
| --- | --- | --- | --- |
| monthly momentum, 10 symbols | 10 | 0.8× | ~0.8% /year |
| daily MA cross, 1 symbol | 2 | 2.5× | ~3% /year |
| daily z-score reversion, 20 symbols | 60 | 6.0× | ~7% /year |

## Defaults (put these in the config, not in the code)

| Instrument class | fee_bps | slippage_bps |
| --- | --- | --- |
| liquid US ETF | 0.5 | 1.0 |
| large-cap equity | 0.5 | 2.0 |
| mid/small cap | 1.0 | 8.0 |
| crypto major | 5.0 | 5.0 |

## The reporting obligations

1. **Breakeven cost**: the bps at which CAGR crosses zero. Publish in every verdict.
2. **Annual cost drag**: `turnover_annual × cost_bps`, in the tearsheet.
3. **Execution sensitivity**: the difference between `next_open` and `next_close` results,
   reported as structural cost. For most daily strategies this dominates the fee.
4. **Trade-level attribution**: each row of `trades.csv` carries the cost charged (both legs),
   so the trade table reconciles with the equity curve's total cost drag (within rounding:
   size changes inside a holding period are attributed to the trade, not to the entry/exit only).

## Common modelling mistakes (each one is in the spot-it-wrong quiz)

- Charging costs once per trade instead of per turnover unit.
- Applying costs after computing Sharpe (optimising gross, reporting net).
- Using the same bps for a liquid ETF and a small cap.
- Forgetting that a flip is two legs (exit + entry).
- Modelling slippage as a constant per bar regardless of turnover.
