# Tearsheet template (Week 4+)

> Produced by `engine/tearsheet.py`. One file per backtest, never hand-written.
> Every number must trace to a saved artifact in `reports/backtests/<name>/`.

```markdown
# <strategy_id> — <name>

spec `a1b2c3d4` · data `e5f6a7b8` · <start> → <end> · <n> bars · costs <fee>+<slip> bps · <execution>

## Headline (out-of-sample)
<CAGR, vol, Sharpe, Sortino, MaxDD, Calmar, Ulcer, turnover, trades>

## In-sample vs out-of-sample
| metric | IS | OOS | verdict |
| --- | --- | --- | --- |
<same metrics on both windows; flag any OOS/IS Sharpe ratio below 0.5>

## Equity and drawdown
<equity curve + drawdown chart, or the CSV path when plotting is unavailable>

## Worst 5 drawdowns
<start, trough, recovery, depth, bars underwater>

## Monthly returns
<year x month grid>

## Trade anatomy
<n trades · avg hold · win rate · expectancy · profit factor · payoff ·
 max win/loss streak · largest trade as % of total PnL>

## Cost sensitivity
<CAGR/Sharpe at 0/5/10/20/30 bps; breakeven bps>

## Fragility
<bootstrap CI of Sharpe; parameter plateau summary; concentration of PnL>

## What this does not tell you
<regime dependence, capacity, data caveats - write them, every time>
```
