# PyTrades — AI Trading Strategy Bootcamp

A 13-week, self-paced, project-driven course that takes you from raw price CSVs to a public
repository containing a backtester you wrote, 15+ strategy verdicts net of costs, a graveyard of
autopsied failures, three paper replications, 30+ days of live paper trading, and a writeup a
stranger can follow.

**This repo is the course itself.** The student workspace is the scaffold in
[`bootcamp/shared/repo-scaffold/`](bootcamp/shared/repo-scaffold/README.md) — copy it, and the
course builds a trading research repo inside your copy.

## Start here

1. [`bootcamp/README.md`](bootcamp/README.md) — what the course is and how to use it.
2. [`bootcamp/syllabus.md`](bootcamp/syllabus.md) — the full index: 13 weeks, 25 concepts,
   18 deliverables, gates, grading, package tree.
3. [`bootcamp/phases/01-foundation/week-01.md`](bootcamp/phases/01-foundation/week-01.md) — today's
   task. The course begins with a data pipeline, not a theory lecture.

## The shape of it

| Phase | Weeks | You build | Milestone |
| --- | --- | --- | --- |
| 1 Foundation | 1-2 | data pipeline, metrics vocabulary, three debunked viral strategies | M1 — debunk a strategy in 30 minutes |
| 2 Engine | 3-4 | your own event-driven backtester, costs, walk-forward, tearsheets | M2 — idea to verdict in under 30 minutes |
| 3 Strategy Factory | 5-6 | six families, six verdicts, sensitivity grids, bootstrap CIs | M3 — 6 tested, 3+ buried, ≥1 survivor |
| 4 Paper Replication | 7-9 | TSMOM, pairs trading, vol-managed portfolios vs their papers | M4 — replications with deviation logs |
| 5 Risk & Portfolio | 10 | sizing rules, allocation, Monte Carlo, regime lab | (feeds the live policy) |
| 6 Live Paper | 11-12 | scheduled bot, daily logs, reconciliation | M5 — 30 days live, divergence explained |
| 7 Synthesis | 13 | public repo, writeup, portfolio doc, graveyard taxonomy | M6 — a stranger can clone and understand it |

## What makes it a course rather than a reading list

- **Build first, theory second.** The 25 concept injections arrive exactly when a failure makes
  them necessary (📐 concept, formula, 3-5 lines of runnable code, example on *your* strategy, a
  time box, and a done-when that requires coding, explaining and spotting a wrong version).
- **Failure is graded.** The graveyard is required every week, and its ranked taxonomy is the
  course's most valuable output.
- **Costs, out-of-sample, verdict — non-negotiable.** No strategy ships without all three.
- **Gates are ship-or-don't-advance**, enforced by `make gate WEEK=n` in your own repo.
- **Live paper trading is mandatory**, and the 30-day clock starts in Week 5 so it can actually
  elapse before the capstone.

Deliberately out of scope: options pricing, stochastic calculus, HFT/microstructure, reinforcement
learning for trading, production infrastructure, and anything PhD-level. The point is to finish
with working artifacts you understand end to end.

## Verifying the course package

The course is itself a tested artifact:

```bash
python bootcamp/tools/verify_course.py      # structural acceptance test (14 check groups)
python bootcamp/tools/test_the_course.py    # mutation suite: proves the verifier bites
python bootcamp/tools/build_syllabus.py     # regenerates the syllabus tables
python bootcamp/tools/sync_gates.py         # regenerates the student repo's gates.json
```

## Repository layout

```
bootcamp/            the course: README, syllabus, registry.json (single source of truth)
  phases/01…07/      weeks, gates, deliverables, concepts, milestones, phase rubrics
  shared/            the student repo scaffold, reference kit, templates, sample data
  capstone/          writeup, portfolio and recall-test templates, capstone rubric
  tools/             course build + verification tools
```
