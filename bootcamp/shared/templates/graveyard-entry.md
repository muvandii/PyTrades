# Graveyard entry template

The graveyard is a required artifact, not a confession. Each entry is 6 lines and
must name a **mechanism** - "it didn't work" is not a cause of death.

Append to `graveyard.md` using this block:

```markdown
## <STRATEGY_ID> - <short name>

- **Died:** YYYY-MM-DD, Week N
- **Cause of death:** <one of: no edge / cost death / look-ahead illusion / overfit /
  regime dependence / data problem / operational death / thesis wrong / insufficient sample>
- **The test that killed it:** <the specific number, e.g. "OOS Sharpe -0.2 after 8 bps costs">
- **Breakeven cost:** <bps round-trip at which the edge vanished, or "n/a">
- **What I'd need to believe it again:** <one falsifiable sentence>
- **Evidence:** reports/backtests/<name>/ · strategies/<id>/verdict.md
```

## Cause-of-death taxonomy (use these words so Week 13 can count them)

| Cause | Looks like | Typical culprit |
| --- | --- | --- |
| no edge | OOS Sharpe ~0, ties with random entries | the idea was not real |
| cost death | positive gross, negative net | turnover too high for the venue |
| look-ahead illusion | beautiful OOS that dies live; signal uses future data | missing shift(), bfill, full-sample stats |
| overfit | great in-sample, negative OOS | parameter sweep selected on the best |
| regime dependence | works in 2010-2021 only | vol/rate regime, one policy era |
| data problem | too good to be true; suspicious gaps, splits, delistings | unvalidated CSV, survivorship |
| operational death | backtest fine, live PnL absent | missed runs, stale bars, timezone bugs |
| thesis wrong | mechanism story does not survive contact | crowded trade, structural change |
| insufficient sample | t-stat 1.1 on 12 trades | not dead, just unproven |
