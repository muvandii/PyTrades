---
week: 8
phase: P4
title: Replicate a Paper - Pairs Trading
deliverables: [D13]
concepts: [C18]
milestone: M4
hours: 18-22
---

# Week 8 — Replicate a Paper: Pairs Trading

## Learning objective

Rebuild the Gatev-Goetzmann-Rouwenhorst pairs result, but with a *test* for the relationship instead of a hope - cointegration, half-life, z-score rules - and with pair selection done on training data only.

## Deliverable

- [D13 — Replication R2: Pairs Trading](deliverables/D13.md): `papers/R2_pairs/impl.py`, `comparison.md`, `deviations.md`.

## Daily tasks

### Mon — Read the dossier, define the universe of candidate pairs

1. Work through [dossiers/R2-pairs-trading.md](dossiers/R2-pairs-trading.md): the formation period, the trading period, the distance metric the paper uses, and the reported Sharpe after costs.
2. Build a candidate list: 20-40 pairs from a coherent sector set (staples, airlines, banks, oil majors, gold miners...). Write down why each pair has an economic link - "both start with the same letter" is not a link.
3. Split your sample in half. Formation/selection on the first half only; the second half is untouched until Friday.

*Time: 3-4 h.*

### Tue — Cointegration and half-life (C18)

1. Inject [C18 — Cointegration & Spreads](concepts/C18-cointegration-and-spreads.md).
2. `papers/R2_pairs/impl.py` part 1: on the formation window, for each candidate pair, estimate the hedge ratio (OLS on log prices), run an Engle-Granger style test (statsmodels `coint`, or ADF on the residual spread), and compute the spread's half-life.
3. Rank the pairs. Report the count that passed and the count that failed - the failures are evidence, not noise.

*Time: 5-6 h.*

### Wed — Build the trading rule

1. Part 2 of `impl.py`: z-score of the spread; enter at |z| ≥ 2, exit at |z| ≤ 0.5, stop out if z exceeds 3.5 (a break, not a bargain) or after a maximum holding period.
2. Two-leg positions: 0.5 gross each side, dollar-neutral from the hedge ratio; costs charged on both legs. Run it on the second half of the sample.
3. Watch the cost line: a pairs trade pays four spreads (two entries, two exits). Estimate the annual drag before you look at the equity curve.

*Time: 4-5 h.*

### Thu — Break it the way real pairs break

1. **Selection look-ahead**: re-run with pairs selected on the *whole* sample. Compare Sharpes. The gap is your selection look-ahead, measured in Sharpe units - write it down.
2. **Break test**: for each traded pair, plot the spread over the OOS window only. Count how many relationships failed (spread wanders, never returns). That count is the strategy's real risk.
3. **Universe sensitivity**: drop the best pair. Drop the best two. Does the strategy survive?

*Time: 4-5 h.*

### Fri — Comparison and deviation log

1. `papers/R2_pairs/comparison.md` with the required evidence: cointegration test output, the chosen pairs, the z-score rules, the walk-forward run where selection used training data only, and the look-ahead gap measured Thursday.
2. `papers/R2_pairs/deviations.md` from the template: universe, formation length, distance metric vs cointegration, cost assumption, trade frequency.

*Time: 3-4 h.*

### Sat — Verdict and registry

1. Verdict paragraph: does the relative-value effect pay after costs on your data, and under what conditions does it stop paying?
2. Any pair that broke permanently gets a graveyard entry with cause `thesis wrong` (the economic link was wrong) or `regime dependence`.
3. Update `strategies/index.md` and `graveyard.md`.

*Time: 3-4 h.*

### Sun — Journal and gate

1. `make gate WEEK=8`: cointegration evidence present in the writeup, selection done on training data only.
2. Journal: how much of your in-sample pairs edge survived honest selection? What does that tell you about the S06 result from Week 6?

*Time: 2-3 h.*

## Gate

`make gate WEEK=8` - see [gates/week-08-gate.md](gates/week-08-gate.md). **Checkpoint:** `comparison.md` includes cointegration evidence, the chosen pairs, spread z-score rules, and a walk-forward run with selection on training data only.

## Graveyard prompt

Half your candidate pairs will fail the test inside the OOS window. Log those failures as evidence that selection-on-full-sample is a look-ahead machine, and note how many pairs the *simplest* distance metric would have picked incorrectly.

## Concept injections this week

- [C18 — Cointegration & Spreads](concepts/C18-cointegration-and-spreads.md) — triggered by a "reversion" trade that turned into a trend trade against you
