# Phase 2 rubric — Engine (Weeks 3-4)

| Criterion | 0 (not yet) | 1 (passing) | 2 (strong) | If you scored low |
| --- | --- | --- | --- | --- |
| **Execution discipline** | signal and trade share a bar | one documented shift; contract tests pass | time-travel test passes and the shift premium is measured and reported | find every `.shift(` in your repo and justify or remove each |
| **Accounting** | weights treated as positions | cash + quantities tracked; buy-and-hold within 1% | `trades.csv` reconciles with the equity curve's cost drag | add an assertion: `|sum(trade costs) − total_cost_drag| < tolerance` |
| **Costs** | applied in the report | charged on turnover inside the loop | breakeven bps published for every strategy; open-vs-close structural cost measured | re-run the bps grid and check the breakeven interpolation |
| **Out-of-sample** | one in-sample number | splits implemented, pooled OOS reported | degradation ratio + parameter-stability table in the tearsheet | report the worst split as well as the pooled number |
| **Tearsheets** | hand-written markdown | generated, all sections present | includes "what this does not tell you" filled with real caveats | add the caveat paragraph for the next strategy before looking at its numbers |
| **Documentation** | `engine/README.md` missing | modules and behaviours documented | records what changed and which numbers moved when it changed | write the change log entry for your last three commits |
| **Graveyard** | nothing died | deaths logged with breakeven bps | causes cluster: "all cost deaths share turnover > 4×/yr" | reopen the entries and add the one number that would have predicted the death |

## Phase 2 retro

Write `reports/retro-P2.md` (three questions from `shared/retro-template.md`) **before** starting
Week 5. The most common answers here: the pattern that killed strategies is cost death, the
concept that mattered most is annualisation or the shift, and the thing still being fooled about
is usually "my OOS window is too short to prove anything".

## Pass bar

- M2 passed with a documented timer log
- Contract suite green against `engine.backtest`
- Every strategy run through the engine has `meta.json` with both fingerprints
- You can explain, without notes: why the shift exists, what an artefact's fingerprint proves, and where your costs are charged
