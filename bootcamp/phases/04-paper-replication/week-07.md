---
week: 7
phase: P4
title: Replicate a Paper - Time-Series Momentum
deliverables: [D12]
concepts: [C16, C17]
milestone: M4
hours: 18-22
---

# Week 7 — Replicate a Paper: Time-Series Momentum

## Learning objective

Implement the TSMOM result from [Moskowitz, Ooi & Pedersen (2012)](dossiers/R1-time-series-momentum.md) on your own data, and reconcile your numbers with the paper's claims by naming every deviation - because a replication is a measurement, not a copy.

## Deliverable

- [D12 — Replication R1: Time-Series Momentum](deliverables/D12.md): `papers/R1_tsmom/impl.py`, `comparison.md`, `deviations.md`.

## Daily tasks

### Mon — Read the dossier, write the claim sheet

1. Work through [dossiers/R1-time-series-momentum.md](dossiers/R1-time-series-momentum.md). Extract the core claim, the exact signal, the universe, the sample, and the reported numbers into a claim sheet at the top of `papers/R1_tsmom/comparison.md`.
2. Predict your own result **before implementing**: what Sharpe do you expect on your universe and period, and which deviation (universe? costs? vol scaling?) do you expect to matter most?
3. Write the prediction down. Being wrong here is the point of the week.

*Time: 3-4 h.*

### Tue — Implement the signal exactly, then adapt

1. `papers/R1_tsmom/impl.py`: the paper's rule - sign of the past 12-month excess return, vol-scaled to a 40% annual target, monthly rebalance. Your engine does the rest (`signals → positions → fills → costs`).
2. Run it on a multi-asset ETF universe (SPY, QQQ, IWM, EFA, EEM, TLT, IEF, GLD, DBC, UUP or equivalent). Multi-asset is the point: TSMOM diversifies across markets, not across time.
3. Inject [C16 — Time-Series vs Cross-Sectional](concepts/C16-time-series-vs-cross-sectional.md): what you implemented in S05 was cross-sectional; this is not the same thing, and the difference decides what diversifies what.

*Time: 4-5 h.*

### Wed — Volatility targeting (C17)

1. Inject [C17 — Volatility Targeting](concepts/C17-volatility-targeting.md).
2. Add the vol scaler: position = sign(signal) × target_vol / realised_vol(symbol), capped at your gross limit; realised vol from a 60-day exponentially weighted window.
3. Compare tearsheets with and without scaler. Then check the *cap* behaviour: how often is the cap binding? If rarely, your target vol is low relative to the asset vol.

*Time: 4-5 h.*

### Thu — Break it in the specific ways the paper is vulnerable

1. **Costs**: TSMOM turns over on sign flips and on every vol rescale. Measure the drag. Then ask the harder question: is the vol rescale itself a cost generator? (Often yes - it trades when nothing changed in the signal.)
2. **Period**: run 2005-2020 and 2010-2020 separately. TSMOM's reputation rests heavily on 2008-2014; check what your sample does without it.
3. **Universe**: run your broad universe, then an equities-only subset. If the effect is a bond-and-gold effect on your data, that is a deviation to name.

*Time: 4-5 h.*

### Fri — Write the comparison (D12 core)

`papers/R1_tsmom/comparison.md`: your numbers and the paper's, side by side.

| Row | Paper's claim | Your result | Deviation that explains the gap |
| --- | --- | --- | --- |
| Sharpe | | | |
| Vol | | | |
| Max DD | | | |
| Turnover | | | |
| Sample | | | |

Every row with a gap gets a named deviation from the taxonomy in
[deviations.md](deliverables/D12.md) (universe, period, costs, sizing, data frequency, survivorship).

*Time: 3-4 h.*

### Sat — Deviations log, and your own verdict

1. `papers/R1_tsmom/deviations.md` from `shared/templates/deviation-log.md`: for each deviation, what you did, what the paper did, the direction of the effect, and the size.
2. Write the replication verdict in one paragraph: did TSMOM replicate for you? What is the mechanism it depends on? What is the one number that would have told you before you started?
3. If it failed on your universe, that is a graveyard entry with cause `thesis wrong` or `regime dependence`.

*Time: 3-4 h.*

### Sun — Journal, gate, registry

1. Update `strategies/index.md` with R1 as a strategy (it is one now: a tested rule with a verdict).
2. `make gate WEEK=7`. Confirm `papers/R1_tsmom/{impl.py,comparison.md,deviations.md}` all exist.
3. Journal: what surprised you about the distance between a paper's headline and your own run?

*Time: 2-3 h.*

## Gate

`make gate WEEK=7` - see [gates/week-07-gate.md](gates/week-07-gate.md). **Checkpoint:** `comparison.md` shows your Sharpe and the paper's side by side, with every gap traced to a named deviation (universe, period, vol scaling, costs).

## Graveyard prompt

Replications die too. If TSMOM fails on your universe or period, that is a finding: log the deviation that explains it rather than a verdict on the authors.

## Concept injections this week

- [C16 — Time-Series vs Cross-Sectional](concepts/C16-time-series-vs-cross-sectional.md) — triggered by the TSMOM mechanism your single-instrument backtests could not express
- [C17 — Volatility Targeting](concepts/C17-volatility-targeting.md) — triggered by risk changing by 3× across regimes while your position size stays fixed
