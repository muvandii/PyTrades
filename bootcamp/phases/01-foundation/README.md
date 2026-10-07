# Phase 1 — Foundation (Weeks 1-2)

**Milestone:** [M1 Reality check](milestones/M1-reality-check.md) — debunk a viral strategy, start to written verdict, in 30 minutes.

## What the teacher ships

| Piece | Where | Why it exists |
| --- | --- | --- |
| Repo scaffold | `shared/repo-scaffold/` | you work in one repo for 13 weeks; it must be right on day one |
| Data fetcher | `shared/data-fetcher/` + `kit/data_fetcher.py` | real bars, cached with provenance, validated structurally |
| Metrics module | `shared/metrics-module/` + `kit/metrics.py` | every number the course uses, with 25 hand-computed oracle tests |
| Viral debunk worksheet | [templates/viral-debunk-sheet.md](templates/viral-debunk-sheet.md) | turns a 30-minute debunk into a checklist |
| Offline laboratory | `shared/sample-data/` | six simulated series with planted properties, for when there is no network |

## What the student ships

| Deliverable | Week | Artifact | One thing it teaches |
| --- | --- | --- | --- |
| [D01](deliverables/D01.md) | 1 | `reports/data-validation.md` | validate before you measure |
| [D02](deliverables/D02.md) | 1 | `reports/measurement-lab.md` | an equity curve is a product; expectancy is its atom |
| [D03](deliverables/D03.md) | 2 | `reports/debunks/debunk-01.md` | recompute a published claim, timed |
| [D04](deliverables/D04.md) | 2 | debunks #2-3 + graveyard | name the mechanism, not the disappointment |

## Concepts injected

| Concept | Triggered by | Week |
| --- | --- | --- |
| [C01 — Returns & Compounding](concepts/C01-returns-and-compounding.md) | first equity curve | 1 |
| [C02 — Expectancy & Profit Factor](concepts/C02-expectancy-and-profit-factor.md) | wanting to say "this is good" | 1 |
| [C03 — Win Rate vs Edge](concepts/C03-win-rate-vs-edge.md) | the "90% win rate" headline | 2 |
| [C04 — Sample Size & Base Rates](concepts/C04-sample-size-and-base-rates.md) | an 11-trade claim | 2 |

Total concept time this phase: ~70 minutes. That is the whole point: two weeks of building
before a single formula, and the formulas arrive attached to something you already broke.

## The loop, in practice

```
PICK    a claim worth 30 minutes (Mon)
BUILD   the smallest codable version (Tue)
MEASURE reproduce its own numbers (Tue-Wed)
BREAK   execution -> costs -> sample (Wed)
DIAGNOSE which killer fired (Wed-Fri)
LEARN   the concept that explains the failure (C01-C04)
REBUILD with the concept applied, on claim #2
VERDICT debunked / survives / inconclusive
LOG     graveyard entry + journal + timed fire drill
```

## Gate

Week 1: [gates/week-01-gate.md](gates/week-01-gate.md) · Week 2: [gates/week-02-gate.md](gates/week-02-gate.md).
Self-grading for the phase: [rubric.md](rubric.md).
