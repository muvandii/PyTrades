# Phase 1 rubric — Foundation (Weeks 1-2)

Self-graded. Score each row, then read the "if you scored low" column *before* moving on:
Phase 2 gives you a backtester, and a backtester multiplies whatever measurement habits you
bring to it.

| Criterion | 0 (not yet) | 1 (passing) | 2 (strong) | If you scored low |
| --- | --- | --- | --- | --- |
| **Data provenance** | CSVs exist, no meta files | every symbol has a `.meta.json` with provider, hash, range | you can explain which row would change a verdict and why the hash matters | re-run `make data --refresh` and inspect one sidecar field by field |
| **Validation honesty** | warnings ignored or hidden | warnings listed with accept/exclude decisions | a tamper test documents what the validator catches and where it is blind | break a CSV on purpose, run `make validate`, write what it missed |
| **Compounding** | total return computed by summing | `(1+r).prod()-1` used consistently | you can derive the recovery formula from the loss arithmetic | redo Week 1 Wed with the notebook closed |
| **Expectancy** | win rate quoted as a quality measure | expectancy + profit factor tabulated per rule | breakeven win rate used to read a claim you have never seen | compute breakeven win rate for every claim you met this phase |
| **Debunk process** | ad-hoc, untimed | template followed end to end | first debunk under 30 minutes, one cold fire drill within 48 h | re-run the checklist on a fourth claim; trim the reconstruction step |
| **Graveyard quality** | "didn't work" | taxonomy cause, evidence link | causes are specific enough to cluster (all cost deaths share a turnover signature) | reopen each entry and replace the cause with a measured test |
| **Journal** | skipped days | 5+ entries/week with numbers | the "fooling myself" line names something concrete you have not tested | backfill honestly; the line does not need to be flattering |

## Phase 1 retro (do this before starting Week 3)

Write `reports/retro-P1.md` answering the three retro questions in
`shared/retro-template.md`. Keep it under a page. Phase 4's gate (G9.5) checks that a retro
exists; starting the habit now means you are not learning it in Week 9.

## Pass bar

- Every "0" is resolved before Week 3 Day 1.
- M1 passed with a documented timer log.
- At least two graveyard entries with taxonomy causes.
- You can state, without notes: what compounding is, what expectancy is, why 90% is not an edge, and why 11 trades is not evidence.
