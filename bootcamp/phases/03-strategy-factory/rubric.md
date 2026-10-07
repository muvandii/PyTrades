# Phase 3 rubric — Strategy factory (Weeks 5-6)

| Criterion | 0 (not yet) | 1 (passing) | 2 (strong) | If you scored low |
| --- | --- | --- | --- | --- |
| **Volume** | < 4 verdicts | 6 verdicts, one per family | 8+ verdicts, including at least one you invented | run two more families from your own reading list |
| **Verdict quality** | "seems to work" | number + mechanism + kill criteria | a stranger could re-run it from the verdict alone | add the artifact path to every number |
| **Cost realism** | gross numbers reported | net numbers, breakeven bps per strategy | breakeven published and compared to the instrument's actual spread | state the spread you are assuming, and why |
| **Graveyard** | empty or one line | 3+ entries with taxonomy causes | entries cluster: a shared cause is named across deaths | write the "what would have predicted this" line for each entry |
| **OOS discipline** | IS only | pooled OOS reported | degradation ratio tracked across all six | compute OOS/IS for every strategy, even the dead ones |
| **Fragility** | single parameter set | one sweep per survivor | plateau width + bootstrap CI + drop-best-year | measure plateau width in parameter units, not "looks stable" |
| **Self-critique** | audit missing | seven questions answered | the audit changed a verdict word or a kill criterion | answer question 1 honestly (count the specs you tried) |
| **Registry** | absent | one row per strategy with linked evidence | the five-line summary names the most common cause of death | check every number traces to a saved artifact |

## Phase 3 retro

Write `reports/retro-P3.md` using the three questions from `shared/retro-template.md`. Typical
answers: "the pattern that killed most strategies was turnover I chose before I looked at spreads",
"the most valuable concept was the bootstrap", "what I am still fooling myself about is the size
of my OOS window".

## Pass bar

- M3 passed (either branch: a survivor with a CI excluding zero, or a documented no-survivor result)
- Six verdicts, each with net-of-cost OOS numbers and a graveyard line
- `strategies/index.md` where every number traces to an artifact
- At least one strategy killed *by you* on evidence, not by the market on a random Tuesday
- The live paper clock is running and has at least a week of history
