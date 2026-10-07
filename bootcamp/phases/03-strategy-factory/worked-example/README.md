# Worked example — a complete S03 package, start to grave

This is a full strategy package in the shape you are expected to produce, so that "done" has a
concrete meaning instead of a vibe. Everything here was produced by running the shipped template
signal on the course's **laboratory data** (`shared/sample-data/LAB_MR.csv`), with the numbers
copied straight out of the run's artifacts.

> **Honesty note (read this before copying anything).** LAB_MR is synthetic data with a planted
> reversion process, so a *lab* verdict can never be market evidence. That is exactly why it is a
> good teaching example: the mechanics of a cost death are visible and reproducible without
> waiting for the market to cooperate. Replace the universe with real data and the analysis with
> your own run before writing a verdict that claims anything about markets.

## The package

| File | What it is |
| --- | --- |
| [config.json](config.json) | the spec: id, universe, params, thesis, tags, exposure |
| [signal.py](signal.py) | `generate(prices, params)` → target weights, no engine imports |
| [tearsheet.md](tearsheet.md) | generated output: headline, IS/OOS, cost sweep, anatomy, caveats |
| [verdict.md](verdict.md) | the written conclusion, including the graveyard line |
| [graveyard-entry.md](graveyard-entry.md) | the autopsy: cause, killer number, lesson |

## Reproduce it

```bash
mkdir -p strategies/S03_worked && cp signal.py strategies/S03_worked/signal.py
cp config.json config/S03_worked.json
cp <course>/shared/sample-data/LAB_MR.csv data/LAB_MR.csv
make run E=engine.backtest S=S03_worked NAME=s03_worked_net20 FEE=10 SLIP=10
make costs S=S03_worked
make tearsheet S=S03_worked
```

## What to notice (the three things this example is teaching)

1. **The gross signal is not stupid.** Gross Sharpe 0.47, win rate 59%, profit factor 1.26. A
   student who stopped at the gross run would have written "small but real edge" and moved on.
2. **Costs are not a haircut, they are the verdict.** Turnover is 38×/year. At a 16 bps
   round-trip the edge is exactly gone; the run at 20 bps is *negative*, with a 54% drawdown. The
   same signal, the same data, two opposite conclusions — decided entirely by a cost assumption.
3. **The autopsy is arithmetic, not opinion.** The graveyard entry contains the killer number
   (breakeven ≈ 15.7 bps vs. an assumed 20 bps), so anyone can re-check the death.

## The counter-example in the same family

The loose version of the same signal — `entry_z = -2.0`, `window = 20`, on the same lab series —
turns over 8.3×/year instead of 38×/year, and it *survives* every cost level in the standard
sweep (Sharpe 0.54 → 0.31 from 0 to 30 bps). Same family, same data, one parameter decision:
the difference between a dead strategy and a live one here is patience.
