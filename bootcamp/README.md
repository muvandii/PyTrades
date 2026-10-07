# AI Trading Strategy Bootcamp — the course

**13 weeks. 7 phases. One public repository.**

You will build a backtesting engine, test 15+ strategies (and kill most of them), replicate three
academic papers, size and combine what survives, run one strategy on live paper trading for 30
days, and publish the whole thing - including the graveyard.

This directory is the course. The `shared/repo-scaffold/` directory inside it is the student repo
you will work in: it contains the reference kit, the gate checker, the journal tool, and the tests.

## Read these two files first

| File | Why |
| --- | --- |
| [syllabus.md](syllabus.md) | the index: weeks, concepts, deliverables, grading, the package tree |
| [phases/01-foundation/week-01.md](phases/01-foundation/week-01.md) | what to actually do today |

## The shape of the course

| Phase | Weeks | What you build | Milestone |
| --- | --- | --- | --- |
| [1 Foundation](phases/01-foundation/README.md) | 1-2 | data pipeline, metrics, three debunked viral strategies | M1: debunk in 30 minutes |
| [2 Engine](phases/02-engine/README.md) | 3-4 | your own event-driven backtester with costs and OOS | M2: idea to verdict under 30 minutes |
| [3 Strategy Factory](phases/03-strategy-factory/README.md) | 5-6 | six strategies across six families, with verdicts | M3: 6 tested, 3 buried, 1 survivor |
| [4 Paper Replication](phases/04-paper-replication/README.md) | 7-9 | TSMOM, pairs, vol-managed - compared to their papers | M4: 2-3 replications with deviation logs |
| [5 Risk & Portfolio](phases/05-risk-portfolio/README.md) | 10 | sizing rules, allocation, Monte Carlo, regime lab | (feeds the live policy) |
| [6 Live Paper](phases/06-live-paper/README.md) | 11-12 | scheduled bot, daily logs, reconciliation | M5: 30 days live + divergence explained |
| [7 Synthesis](phases/07-synthesis/README.md) | 13 | public repo, writeup, portfolio doc, graveyard taxonomy | M6: a stranger can clone and understand it |

## The non-negotiables

1. **Build first, theory second.** Concepts arrive when a failure makes them necessary.
2. **Costs, out-of-sample, verdict.** No strategy ships without all three.
3. **Failure is graded.** The graveyard is required, and its taxonomy is your most valuable artifact.
4. **Gates are ship-or-don't-advance.** They check artifacts, not intentions.
5. **Ugly-but-running beats pretty-but-hypothetical.**

## How to use this package

**If you are the student:**

- Work inside a copy of `shared/repo-scaffold/` (see its README for setup). Daily rhythm and
  weekly tasks live in `phases/<phase>/week-NN.md`; gates in `gates/week-NN-gate.md`.
- Use the templates in `shared/templates/` for verdicts, graveyard entries, tearsheets, theses,
  deviation logs and reconciliations. Use `shared/journal-template.md` daily.
- Check yourself with the gate checker (`make gate WEEK=n`) and the phase rubric at the end of each
  phase. There is no external grader: the artifacts either exist or they do not.

**If you are a teacher or a study group:**

- Each phase ships a `rubric.md` and the gates carry both automated and manual checks. Week files
  include time boxes so you can set a realistic pace; the milestones are the cohort checkpoints.
- `phases/02-engine/instructor/OPTIONAL-instructor-notes.md` shows what to look for when reviewing
  an engine build; it is optional material and the course is complete without it.

## Verifying the course package itself

The course is a build artifact with its own tests:

```bash
python bootcamp/tools/verify_course.py      # structural acceptance test
python bootcamp/tools/test_the_course.py    # proves the verifier bites (mutations)
python bootcamp/tools/build_syllabus.py     # regenerates syllabus tables
python bootcamp/tools/sync_gates.py         # regenerates shared/repo-scaffold/gates.json
```

## Where the time goes

Roughly 14-22 hours per week: 3-5 hours of building on weekdays, 4-6 on one weekend day, plus a
concept injection and a journal entry. The course is designed to be completed solo and self-paced -
no cohort, no lectures, no video.

## The one-sentence version

Build the measurement apparatus, use it to destroy most of your ideas, keep the survivors honest
with costs and out-of-sample evidence, run one of them live in public, and publish everything
including what failed.
