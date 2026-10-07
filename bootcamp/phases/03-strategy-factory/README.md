# Phase 3 — Strategy Factory (Weeks 5-6)

**Milestone:** [M3 Strategy factory](milestones/M3-strategy-factory.md) — 6 strategies tested, 3+ in the graveyard, at least one survivor with out-of-sample evidence.

## What you leave with

Six strategies from six different families, each with a generated tearsheet, a written verdict
and (usually) a graveyard entry; a registry table that makes your track record readable at a
glance; and an overfitting audit of your own best result that you wrote yourself, against your
own interest.

## The six families, and what each one teaches

| id | Family | Template | Expected fate |
| --- | --- | --- | --- |
| S01 | trend, MA cross | [templates/signal_S01_ma_cross.py](templates/signal_S01_ma_cross.py) | survives; modest edge or a tie with buy-and-hold |
| S02 | reversion, RSI | [templates/signal_S02_rsi_reversion.py](templates/signal_S02_rsi_reversion.py) | likely `cost death` (25×/yr turnover) |
| S03 | Bollinger / z-score | [templates/signal_S03_bollinger.py](templates/signal_S03_bollinger.py) | gross ~1.0 Sharpe, net near zero |
| S04 | breakout, Donchian | [templates/signal_S04_donchian.py](templates/signal_S04_donchian.py) | low win rate, profit factor ~1, cost-tolerant |
| S05 | cross-sectional momentum | [templates/signal_S05_momentum.py](templates/signal_S05_momentum.py) | the most likely survivor |
| S06 | pairs, rolling hedge | [templates/signal_S06_pairs.py](templates/signal_S06_pairs.py) | works in-sample, decays later |

Spec templates live in `templates/configs/`; the copy-run-verdict procedure is described in
[templates/strategy-templates.md](templates/strategy-templates.md).

## The worked example

[worked-example/](worked-example/README.md) contains a complete package — config, signal,
tearsheet, verdict, graveyard entry — for a tight Bollinger variant on the laboratory series. It
is a real run with real numbers, and it dies of cost death in the most instructive way available:
the same family, one parameter decision, alive on one side of the spread and dead on the other.
Study the shape of the verdict before writing your own; then never copy its numbers.

## Concepts injected

| Concept | Trigger |
| --- | --- |
| [C11 — Sortino & Downside Deviation](concepts/C11-sortino-and-downside-deviation.md) | Sharpe near zero, small losses, lumpy gains |
| [C12 — Bootstrap & CIs](concepts/C12-bootstrap-and-confidence-intervals.md) | ranking two survivors 0.13 apart |
| [C13 — Parameter Sensitivity & Plateaus](concepts/C13-parameter-sensitivity-and-plateaus.md) | one grid smooth, another spiky |
| [C14 — t-test Intuition](concepts/C14-t-test-intuition.md) | is +0.031%/day real? |
| [C15 — Overfitting & Walk-Forward Honesty](concepts/C15-overfitting-and-walkforward.md) | IS 2.1, OOS −0.2 |

## Deliverables

| | Week | Artifact |
| --- | --- | --- |
| [D08](deliverables/D08.md) | 5 | Strategies S01-S03 with tearsheets and verdicts |
| [D09](deliverables/D09.md) | 5 | Strategy registry + graveyard v1 |
| [D10](deliverables/D10.md) | 6 | Strategies S04-S06 + bootstrap confidence intervals |
| [D11](deliverables/D11.md) | 6 | Overfitting audit + sensitivity heatmaps |

## Gates

Week 5: [gates/week-05-gate.md](gates/week-05-gate.md) · Week 6: [gates/week-06-gate.md](gates/week-06-gate.md) ·
Self-grading: [rubric.md](rubric.md)

## The thing this phase is really teaching

A strategy pipeline is a *filter*, and its job is to destroy ideas. If nothing has died by the end
of Week 5, the filter is broken - usually because costs are too kind, the out-of-sample window is
the same as the in-sample window, or the verdict is being written from memory instead of from an
artifact. Students who finish Phase 3 with six verdicts and four graves are doing the course
correctly; students with six survivors are not.
