# Phase 5 — Risk & Portfolio (Week 10)

**Milestone connection:** the risk policy built here is what the live bot trades in Phase 6; M5 (30 days of live paper trading with reconciliation) is confirmed in Week 12.

## What you leave with

A one-page risk policy you can actually implement, a portfolio whose combination arithmetic you
have measured rather than assumed, a ruin probability under your *own* rules, and a regime lab
that separates "the strategy stopped working" from "the market changed".

## The four reports (D15)

| Report | Question it answers |
| --- | --- |
| [risk-policy.md](../../shared/repo-scaffold/) one page | what are the rules, with numbers, that the bot will trade? |
| [portfolio-allocation.md](../../shared/repo-scaffold/) | how do the survivors combine, and what did correlation do to the combination? |
| [monte-carlo.md](../../shared/repo-scaffold/) | under these rules, how often does this blow up? |
| [regime-lab.md](../../shared/repo-scaffold/) | in which environments does each strategy earn, and is a filter worth its switches? |

(The four reports live in your working repo at `reports/`, not in the course tree.)

## Concepts injected

| Concept | Trigger |
| --- | --- |
| [C20 — Correlation & Portfolio Variance](concepts/C20-correlation-and-portfolio-variance.md) | two Sharpe-1.4 strategies combining into something worse than either |
| [C21 — Kelly & Fractional Kelly](concepts/C21-kelly-and-fractional-kelly.md) | an edge with no size |
| [C22 — Risk of Ruin](concepts/C22-risk-of-ruin.md) | an optimal sizing with an intolerable path |

## Deliverable and gate

[D15](deliverables/D15.md) · [gates/week-10-gate.md](gates/week-10-gate.md) · [rubric.md](rubric.md) ·
[M5 definition](../06-live-paper/milestones/M5-live-paper.md)

## The design principle for this week

Sizing rules are the most fragile artifacts in the whole course, because they fail *silently*: a
badly sized good strategy produces a mediocre equity curve, and the student concludes the
*strategy* was mediocre. The Monte Carlo exists to catch that mistake before the market does, and
the one-page policy exists so that the rules that size your capital are the rules you actually
wrote, not the ones you improvised on a bad Tuesday.
