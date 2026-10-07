# Phase 5 rubric — Risk & portfolio (Week 10)

| Criterion | 0 (not yet) | 1 (passing) | 2 (strong) | If you scored low |
| --- | --- | --- | --- | --- |
| **Policy writability** | rules scattered across reports | one page, quantified rules | every rule has a threshold, an action and (for de-risking) a resume condition | delete every adjective; replace with a number or a formula |
| **Sizing correctness** | position size chosen by feel | sizing from vol target and/or fractional Kelly | sizing sensitivity grid shows the choice is a plateau, not a knife edge | sweep target vol and Kelly fraction; plot Sharpe and max DD |
| **Correlation honesty** | full-sample correlation only | common-overlap correlation reported | crisis correlation measured separately and used to size | compute correlation in the worst 10% of months |
| **Survival** | ruin assumed acceptable | P(50% DD) simulated under your rules | de-risking rule tested in simulation and shown to reduce ruin probability | re-run the Monte Carlo with the policy's de-risking applied inside the paths |
| **Regime honesty** | filters chosen with hindsight | regime split by a causal rule | filter's OOS effect quantified, including its switching cost | count the switches and multiply by the cost per switch |
| **Allocation** | equal weights, no analysis | combination vs equal-weight measured on the same window | weights justified by correlation structure and cost | check the overlap window first; allocation across unequal windows is a bug |
| **Policy/simulation consistency** | rules in the policy not present in the simulation | every policy rule exercised in Monte Carlo | simulation's worst path traced back to a specific rule | list the policy rules and tick which are simulated |

## Phase 5 retro

This phase has no separate retro check in the gates — it is covered by the Week 9 and Week 12
retros that bracket it. If you want one anyway (recommended), append three answers to
`reports/retro-P4.md` or start `reports/retro-P5.md`: the sizing rule that died, the concept that
changed your numbers most, and the assumption about your own tolerance you have not tested.

## Pass bar

- Four reports present, cross-referenced, and consistent with each other
- Ruin probability computed under the policy's own rules (a raw-return simulation does not count)
- Sizing sensitivity saved as 3+ CSVs
- The policy fits on one page and can be implemented in code without further interpretation
- At least one sizing idea was killed and logged in the graveyard
