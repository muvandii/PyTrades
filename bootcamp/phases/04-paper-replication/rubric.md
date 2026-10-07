# Phase 4 rubric — Paper replication (Weeks 7-9)

| Criterion | 0 (not yet) | 1 (passing) | 2 (strong) | If you scored low |
| --- | --- | --- | --- | --- |
| **Specification fidelity** | paraphrased the paper loosely | signal, universe, frequency and sizing match the dossier | deviations from the paper are *chosen* and documented, not accidental | rewrite the spec from the paper's own numbers before coding |
| **Prediction** | none written | prediction recorded before implementing | prediction error analysed: which deviation you underestimated and why | write tomorrow's prediction tonight |
| **Comparison** | prose | table: your numbers beside the paper's | each gap has a class, a direction and an estimated size | build the claim sheet first, then fill the table |
| **Deviation honesty** | gaps unexplained | deviations logged with classes | the deviation that explains the most variance is named as *the* cause | re-run with a single change to isolate the largest gap |
| **Selection discipline** | pairs chosen with full-sample knowledge | selection on the training half, gap measured | the look-ahead gap is quantified in Sharpe units and quoted in the verdict | re-select, re-run, report both |
| **Causality in the numbers** | in-sample vol, contemporaneous σ | strictly trailing estimators everywhere | estimator choice documented next to the number it produced | grep the code for any estimator that touches the current bar |
| **Synthesis** | a summary of three weeks | four questions answered | a mechanism per replication and a rule for the next paper | rewrite with mechanism-first sentences |
| **Phase retro** | missing | three questions answered | a pattern named across all three replications | ten minutes with `shared/retro-template.md` |

## Phase 4 retro

Write `reports/retro-P4.md`. Typical answers: "the pattern that killed results was universe
mismatch - 9 of 12 named deviations were universe or period"; "the most valuable concept was
cointegration, because it turned a hunch into a test with a p-value"; "what I am still fooling
myself about is how much of the TSMOM gross Sharpe I believe on ten correlated ETFs".

## Pass bar

- M4 passed: three (or two) comparisons with deviation logs and a synthesis
- R2 selection performed on training data only, with the gap measured
- R3 uses a causal vol estimator, and the cap/target grid is reported
- No number in any comparison is un-traceable to a saved backtest artifact
- The phase retro is written before Week 10 begins
