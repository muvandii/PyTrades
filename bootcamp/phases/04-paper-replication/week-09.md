---
week: 9
phase: P4
title: Replicate a Paper - Vol-Managed Portfolios
deliverables: [D14]
concepts: [C19]
milestone: M4
hours: 16-20
---

# Week 9 — Replicate a Paper: Vol-Managed Portfolios

## Learning objective

Implement volatility targeting on a multi-asset portfolio, reconcile it with its own replication literature, then close the phase by synthesising all three replications: what replicated, what did not, and why.

## Deliverable

- [D14 — Replication R3 + cross-paper synthesis](deliverables/D14.md): `papers/R3_volmanaged/impl.py`, `comparison.md`, `papers/synthesis.md`, and milestone **M4**.

## Daily tasks

### Mon — Read the dossier (both sides of it)

1. Work through [dossiers/R3-vol-managed-portfolios.md](dossiers/R3-vol-managed-portfolios.md): the Moreira-Muir claim, the mechanism (vol clusters, returns do not scale with vol), and the known replication critiques (estimation error in vol, turnover from rescaling, sensitivity to the vol estimator window).
2. Write your prediction: on which of your assets will vol management help, and on which will it hurt?

*Time: 3-4 h.*

### Tue — Implement vol management properly

1. `papers/R3_volmanaged/impl.py`: exposure scaled by `target_vol / realised_vol` where realised vol is estimated causally (trailing window or EWMA), with a cap and a floor on the scaling factor.
2. Three estimators, same everything else: 20-day simple, 60-day EWMA (span), and 20-day realised-vol from squared returns. If the result depends on the estimator, that is a finding, not a nuisance.

*Time: 4-5 h.*

### Wed — Costs, caps, and the turnover trap

1. Measure turnover of the *unscaled* strategy vs the vol-managed one. Rescaling trades even when the sign never changes: quantify it.
2. Sweep the cap: 1.0 (no leverage), 1.5, 2.0. Then sweep the target vol: 8%, 10%, 12%. Save the grid.
3. Ask the question that kills most vol-management results: does it survive 2× costs on your universe?

*Time: 4-5 h.*

### Thu — Reconciliation against the critique (C19)

1. Inject [C19 — Replication Deviations: Statistical vs Economic Significance](concepts/C19-replication-deviations.md).
2. Write `papers/R3_volmanaged/comparison.md`: paper numbers vs yours, with each gap assigned to one of the five deviation classes from the deviation-log template.
3. The specific C19 exercise: your Sharpe improvement is +0.15 with a bootstrap CI of [−0.1, +0.4]. Is that *statistically* distinguishable from zero? Is it *economically* worth the extra complexity and turnover? Answer both, separately.

*Time: 4-5 h.*

### Fri — Cross-paper synthesis (the real deliverable)

`papers/synthesis.md`, one page, answering:

1. **What replicated?** Which of R1/R2/R3 produced a result in the same direction and rough magnitude as its paper, on your data, net of costs?
2. **What did not?** For each, the single deviation that explains the most variance (not a list - one).
3. **Why?** A mechanism-level answer. "My sample is shorter" is a fact, not a mechanism. "TSMOM needs many uncorrelated futures markets to diversify; ten correlated ETFs cannot express it" is a mechanism.
4. **What did you learn about replication itself?** State it as a rule you will apply to the next paper you read.

*Time: 4-5 h.*

### Sat — M4 audit: is the phase's evidence complete?

Checklist for M4:

- [ ] Three implementations, each committed with its config
- [ ] Three `comparison.md` with your numbers and the paper's side by side
- [ ] Deviation logs naming universe/period/costs/sizing/data-frequency effects
- [ ] Pair selection on training data only (R2)
- [ ] Vol-management result reported with the estimator choice visible (R3)
- [ ] Every replication's fingerprints in `meta.json` (spec + data)
- [ ] `papers/synthesis.md` with the four answers above

*Time: 3-4 h.*

### Sun — Phase retro, journal, gate

1. `reports/retro-P4.md` using the three questions from `shared/retro-template.md`.
2. Journal: which replication taught you the most about your own backtester? (It is usually R2 - two legs, four spreads, and a hedge ratio that drifts.)
3. `make gate WEEK=9`: three comparisons, the synthesis, the retro.

*Time: 2-3 h.*

## Gate

`make gate WEEK=9` - see [gates/week-09-gate.md](gates/week-09-gate.md). **Milestone M4:** 2-3 replications shipped, each with `comparison.md` + `deviations.md`, plus `papers/synthesis.md` answering what replicated, what did not, and why.

## Graveyard prompt

If a paper's Sharpe does not survive your costs and period, the paper is not wrong - you were not trading the paper's asset. Log the gap, not a verdict on the authors. And log the *specific* thing you were trading instead: a different universe, a different era, a different cost structure, or a different notion of what "exposure" means.

## Concept injections this week

- [C19 — Replication Deviations: Statistical vs Economic Significance](concepts/C19-replication-deviations.md) — triggered by replicating 60% of a paper's Sharpe and having to decide whether that counts
