# M3 — Strategy factory (end of Week 6)

## Pass condition

> 6 strategies tested, 3+ in the graveyard, at least 1 survivor with out-of-sample evidence.

Verbatim from the course registry, with the course's operationalisation: the survivor's pooled
OOS Sharpe must sit inside a bootstrap CI that excludes zero. If no strategy survives, M3 passes
with a written statement saying so, backed by six verdicts and the graveyard - the second branch
of the pass condition exists precisely so that honesty is not punished.

## What it proves

That you can produce strategy verdicts at a rate of two or three a week, with the same pipeline
every time, and that you are willing to kill your own ideas on evidence. By Week 13 you need 15+
verdicts; six of them land here.

## Supporting requirements

- Six verdicts, each with net-of-cost OOS numbers and a graveyard line
- `strategies/index.md` with one row per strategy and no number that is absent from an artifact
- Two-parameter sensitivity grids for at least two strategies
- A bootstrap CI for every positive-Sharpe survivor, plus the t-stat and independent-bet count
- The overfitting audit answering all seven questions

## Fail path

| Symptom | Diagnosis | Fix |
| --- | --- | --- |
| fewer than 6 verdicts | the pipeline is not yet frictionless | time one end-to-end run; simplify the spec and tearsheet |
| everything died, no CI computed | you skipped the measurement layer | compute the CI for at least one strategy before concluding anything |
| survivors but no OOS numbers | in-sample optimisation leaked into the verdict | run the walk-forward and report the pooled number only |
| audit answers vague ("it seems robust") | the questions were treated as prose | each answer needs a number and a source artifact |

Remediation before Week 7: Phase 4 hands you a paper to replicate. Replication is the strictest
test of your factory - the paper dictates the specification, so any weakness in your pipeline
shows up as an unexplained gap instead of a dead strategy. Fix the pipeline first.

## Remediate before Week 7

Phase 4 hands you a paper to replicate. Replication is the strictest test of your factory - the
paper dictates the specification, so any weakness in your pipeline shows up as an unexplained gap
instead of a dead strategy. Before starting Week 7: pick your best survivor, re-run it from a cold
spec (copy the config, do not edit the old one), and confirm the number reproduces. If it does
not, fix the pipeline first; the replications will not forgive it.
