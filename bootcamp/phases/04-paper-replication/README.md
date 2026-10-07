# Phase 4 — Paper Replication (Weeks 7-9)

**Milestone:** [M4 Paper replication](milestones/M4-paper-replication.md) — 2-3 replications shipped, each with a comparison and a deviation log, plus a cross-paper synthesis.

## The three dossiers

| | Paper | Core claim | What it teaches you |
| --- | --- | --- | --- |
| [R1](dossiers/R1-time-series-momentum.md) | Moskowitz, Ooi & Pedersen (2012), *Time Series Momentum* | past 12-month excess return predicts the next month, in nearly every futures market | a mechanism needs its universe: TSMOM on three equity ETFs is not TSMOM |
| [R2](dossiers/R2-pairs-trading.md) | Gatev, Goetzmann & Rouwenhorst (2006), *Pairs Trading* | spreads of related assets revert often enough to pay costs | selection on the full sample is a look-ahead machine; test the relationship before you trade it |
| [R3](dossiers/R3-vol-managed-portfolios.md) | Moreira & Muir (2017) + Harvey et al. (2018) critique | scaling exposure inverse to recent vol raises risk-adjusted returns | statistically real is not the same as economically worth it |

## Order of operations (this phase has a rhythm)

1. **Claim sheet first** (Monday): extract the paper's numbers before writing any code.
2. **Prediction before implementation** (Monday): write down what you expect and which deviation
   will matter most. You will be wrong; the size of the error is data about your own priors.
3. **Implement exactly, then adapt** (Tuesday): the adaptation is a deviation, so log it.
4. **Attack it** (Thursday): costs, period split, universe subset, selection look-ahead, estimator
   choice. These are the deviations you will name in the comparison.
5. **Compare and log** (Friday-Saturday): numbers side by side, one named cause per gap.
6. **Synthesise** (Week 9 Friday): what replicated, what did not, why, and the rule you will apply
   to the next paper.

## Deliverables

| | Week | Artifact |
| --- | --- | --- |
| [D12](deliverables/D12.md) | 7 | R1: TSMOM implementation, comparison, deviations |
| [D13](deliverables/D13.md) | 8 | R2: pairs implementation, comparison, deviations |
| [D14](deliverables/D14.md) | 9 | R3: vol-managed implementation + `papers/synthesis.md` |

## Concepts injected

| Concept | Trigger |
| --- | --- |
| [C16 — Time-Series vs Cross-Sectional](concepts/C16-time-series-vs-cross-sectional.md) | the TSMOM mechanism your single-asset tests could not express |
| [C17 — Volatility Targeting](concepts/C17-volatility-targeting.md) | risk swinging 3× while position size stays fixed |
| [C18 — Cointegration & Spreads](concepts/C18-cointegration-and-spreads.md) | a "reversion" trade turning into a trend against you |
| [C19 — Statistical vs Economic Significance](concepts/C19-replication-deviations.md) | 60% of the paper's Sharpe and a decision to make |

## The templates you will reuse

`shared/templates/deviation-log.md` (every gap gets a class, a direction and a size),
`shared/templates/reconciliation.md` (reused in Week 12 for the live/backtest gap), and
`shared/templates/verdict.md` (a replication still gets a verdict word).

## Gates

Week 7: [gates/week-07-gate.md](gates/week-07-gate.md) · Week 8: [gates/week-08-gate.md](gates/week-08-gate.md) ·
Week 9: [gates/week-09-gate.md](gates/week-09-gate.md) · Self-grading: [rubric.md](rubric.md)

## Why replication, before risk and live trading

By Week 7 you have six strategies and a working engine, and the temptation is to go straight to
portfolio construction. Replication is the deliberate detour: it removes the choice of *what* to
test, leaving only the discipline of *how* to test it. Students who skip this phase tend to build
portfolios out of strategies selected by their own preferences; students who do it arrive at Week
10 with a measured, component-level understanding of how much of every result is universe, period,
cost, and sizing - which is precisely the list Week 12 will need to attribute live divergence.
