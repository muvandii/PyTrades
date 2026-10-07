# The cost model, and why it decides most strategies

Costs are not a haircut applied at the end. They are a **per-turnover tax**, and
turnover is a property of the signal, not of your sincerity.

## The formula this course uses

```
cost_per_bar      = turnover_per_bar x (fee_bps + slippage_bps) / 10_000
turnover_per_bar  = sum over symbols of |weight[t] - weight[t-1]|
net_return        = gross_return - cost_per_bar
```

Round-trip figures in the course are fee + slippage already summed per side, so
"10 bps round trip" means roughly 5 bps each way.

## Defaults, and why

| Instrument class | Fee (bps/side) | Slippage (bps/side) | Notes |
| --- | --- | --- | --- |
| Liquid US ETFs (SPY, QQQ, IWM) | 0.5 | 1.0 | ~1 bp spread, no commission at most brokers |
| Large-cap US equities | 0.5 | 2.0 | wider spreads on single names |
| Mid/small caps | 1.0 | 8.0 | 10-50 bps spreads are normal |
| Crypto majors | 5.0 | 5.0 | venue fees dominate |
| Anything you trade daily | — | — | if you do not know the spread, you cannot use it |

**Rule:** model at least 2x your believed cost before writing a verdict. If the edge
only survives at your optimistic number, the edge is your optimism.

## Three questions to ask of every strategy

1. **What is the breakeven cost?** Where CAGR crosses zero. Publish this number in the verdict.
2. **How much does turnover cost per year?** `turnover_annual x cost_bps`. A daily
   rebalancing strategy at 5 bps round trip loses roughly 13%/year to costs alone.
3. **Does the edge live in a part you can actually trade?** If the returns come from the
   10% of bars around earnings, your fills are the problem.

## Bigger than slippage: the gap between close and open

The reference engine fills at the next open by default and splits each bar's return into
overnight (only for positions already held) and intraday (after the fill). If your signal
needs the gap, you must already be positioned before the close it was computed on, which
is impossible. That structural miss is usually larger than the spread you are modelling,
and it is exactly what shows up in Week 12's reconciliation.
