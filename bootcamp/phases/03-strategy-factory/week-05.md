---
week: 5
phase: P3
title: The Factory Floor
deliverables: [D08, D09]
concepts: [C11, C12, C13]
milestone: null
hours: 16-20
---

# Week 5 — The Factory Floor

## Learning objective

Run three signal families through the same pipeline - spec, signal, backtest, tearsheet, verdict, graveyard - and produce comparable artifacts for all three. Also: start the live paper clock, because 30 days is 30 days.

## Deliverable

- [D08 — Strategies S01-S03](deliverables/D08.md): MA cross, RSI reversion, Bollinger - each with tearsheet, verdict, and graveyard entry if dead.
- [D09 — Strategy registry + graveyard v1](deliverables/D09.md): `strategies/index.md` and a graveyard with at least two entries.

## Daily tasks

### Mon — Pick three families and write the theses first

1. Copy the three templates from [templates/](templates/strategy-templates.md) into `config/` and `strategies/`: `S01_ma_cross`, `S02_rsi_reversion`, `S03_bollinger`.
2. For each, write the thesis per `shared/templates/thesis.md` **before running anything**: the claim, who is on the other side, why it persists, what would make it false.
3. Write your prior: which one do you expect to survive costs and OOS, and why.

*Time: 2-3 h. Expect: writing "why it persists" is hard for at least one family - that is the family that will die.*

### Tue — S01 MA cross: build and run

1. Implement or adapt `signal.py` for `S01_ma_cross`. Run `make run E=engine.backtest S=S01_ma_cross NAME=s01_in`.
2. Generate the tearsheet and read it in full.
3. Sanity: is trade frequency plausible for a 50/200 cross on daily bars (a handful per decade)?

*Time: 3-4 h. Trend families are the easiest to implement and the hardest to kill; expect decent gross numbers.*

### Wed — S02 RSI reversion: build, run, then break it with costs

1. Implement `S02_rsi_reversion` (2-period RSI or 14-period, entry below 10-30, exit above 50-70).
2. Run it, generate the tearsheet, then run `make costs S=S02_rsi_reversion`.
3. Start the live paper clock today: create `live/config.json` with the strategy you will run in Week 11, the universe, the sizing rule, and today's date. See [shared/live paper policy](../../registry.json).

*Time: 4-5 h. Expect reversion to look excellent gross and to bleed at 10-20 bps. That is the deliverable's lesson.*

### Thu — S03 Bollinger: the worked example, done your way

1. Read [worked-example/](worked-example/) - a complete S03 package (signal, config, tearsheet, verdict). Notice the shape of the verdict: the number, the mechanism, the kill criteria.
2. Build your own S03 with different parameters, run it, and write your verdict in the same shape.
3. Inject [C11 — Sortino & Downside Deviation](concepts/C11-sortino-and-downside-deviation.md): the reversion family usually has a better Sortino than Sharpe, and you should understand why before you write "no edge".

*Time: 3-4 h.*

### Fri — Parameter perturbation (C13, first pass)

1. For each of the three strategies, sweep the main parameter (MA: slow window 100-250; RSI: entry threshold 5-40; Bollinger: z or std threshold 1.0-3.0) holding everything else fixed.
2. Save the grids as `reports/sensitivity/<id>.csv`.
3. Inject [C13 — Parameter Sensitivity & Plateaus](concepts/C13-parameter-sensitivity-and-plateaus.md). Mark on each grid: plateau or spike?
4. Start the bootstrap: resample the daily returns of each strategy 2,000 times, compute the Sharpe distribution, and record the 5-95% interval. Inject [C12 — Bootstrap & Confidence Intervals](concepts/C12-bootstrap-and-confidence-intervals.md).

*Time: 4-5 h.*

### Sat — Verdicts and the registry (D08, D09)

1. Write three verdicts from `shared/templates/verdict.md`: headline numbers (net, OOS), cost sensitivity, fragility checks, verdict, mechanism, kill criteria, graveyard line.
2. Build `strategies/index.md`: id, family, universe, IS Sharpe, OOS Sharpe, breakeven bps, verdict, link. This table becomes your project's front page.
3. Update `graveyard.md` with every death so far - including Phase 1's baselines.

*Time: 4-5 h.*

### Sun — Phase hygiene, journal, gate

1. `make gate WEEK=5`. Fix failures.
2. Confirm the live clock file exists and is committed (`live/config.json`): the gate checks it.
3. Journal: what did the three families have in common in how they died? (Their failure mode is usually shared by construction.)

*Time: 2-3 h.*

## Gate

`make gate WEEK=5` - see [gates/week-05-gate.md](gates/week-05-gate.md). Requirements: three verdicts, the registry, 2+ graveyard entries, and the live clock started.

## Graveyard prompt

Expect at least one cost death this week. Record the breakeven bps and the annual turnover - and notice whether the death was predictable from the thesis (a high-turnover idea entered into with a "reversion is real" belief was always going to meet the spread). Also note any family that produced a *plateau*: write the plateau's width in the verdict, because it is the strongest evidence you have produced so far.

## Concept injections this week

- [C11 — Sortino & Downside Deviation](concepts/C11-sortino-and-downside-deviation.md) — triggered by two strategies with equal Sharpe but very different downside
- [C12 — Bootstrap & Confidence Intervals](concepts/C12-bootstrap-and-confidence-intervals.md) — triggered by wanting to rank two survivors 0.3 apart
- [C13 — Parameter Sensitivity & Plateaus](concepts/C13-parameter-sensitivity-and-plateaus.md) — triggered by finding the one parameter pair that works
