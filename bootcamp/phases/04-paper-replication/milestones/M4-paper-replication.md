# M4 — Paper replication (end of Week 9)

## Pass condition

> 2-3 papers implemented end-to-end and compared against the paper's claims with a deviation log.

Verbatim from the course registry. "Shipped" means committed, with the implementation, the config
it ran under, and the artifacts the numbers came from.

## What it proves

That you can read a specification written by someone else and produce your own measurement of it -
the core skill of research. It also proves you can hold two ideas at once: the paper may be right
about the market and wrong about your universe, and both statements can be true simultaneously.

## Supporting requirements

- Three implementations (`R1_tsmom`, `R2_pairs`, `R3_volmanaged`), each runnable from its config
- Three comparisons with your numbers beside the paper's, gaps attributed by class
- R2: pair selection on training data only, with the look-ahead gap measured
- R3: a causal vol estimator, the cap/target grid, and a CI on the Sharpe difference
- `papers/synthesis.md` with one mechanism-level answer per replication
- Phase 4 retro (`reports/retro-P4.md`) with the three required questions answered

## Fail path

| Symptom | Diagnosis | Fix |
| --- | --- | --- |
| comparison.md is a paragraph, not a table | the paper's claim was not extracted numerically | write the claim sheet first: Sharpe, vol, DD, turnover, sample |
| "did not replicate" with no deviation named | the interesting half of the work was skipped | for each gap, name one class and estimate its direction and size |
| R2 pairs chosen with full-sample knowledge | the classic look-ahead | re-select on the training half; report both numbers |
| R3 improvement is large and fragile | in-sample vol estimator | recompute with strictly trailing σ; the improvement usually shrinks |
| synthesis.md is a summary | the questions were treated as bookkeeping | answer mechanism-level: why does this universe fail to express that result? |

## Remediate before Week 10

Phase 5 sizes and combines what you have. If your replications produced no usable signal (or
produced one you cannot trust), you will be sizing noise. Before starting Week 10, pick the one
replication whose mechanism you believe, and bring it forward as a candidate for the live
portfolio - with its deviation list attached, because Week 13's writeup will quote it.
