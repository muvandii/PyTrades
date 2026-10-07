# Capstone rubric (D18 / M6)

Weighted like the course: verdicts 30%, backtester 15%, replications 20%, live log 20%,
journal+graveyard 15%. The capstone is where those components become one public artifact.

| Component | 0 | 1 (passing) | 2 (strong) | Evidence |
| --- | --- | --- | --- | --- |
| **Verdicts (30%)** | < 8 verdicts | 15+ verdicts with net-of-cost OOS numbers | every verdict has kill criteria and a mechanism sentence | `strategies/*/verdict.md`, `strategies/index.md` |
| **Engine (15%)** | contract suite red | suite green against your engine, tests documented | time-travel + shift-premium tests, fingerprints in every `meta.json` | `engine/`, `reports/`, `kit/tests/` |
| **Replications (20%)** | < 2 shipped | 2-3 with comparisons + deviation logs | synthesis names a mechanism per replication and a rule for the next paper | `papers/`, `papers/synthesis.md` |
| **Live log (20%)** | no logs | 30+ days, reconciliation with components | components sum within rounding; unexplained < 10%; divergence budget written | `live/` |
| **Journal + graveyard (15%)** | < 40 entries, no taxonomy | 80+ entries, 3-5 ranked causes | each cause has a predictive signal; entries keep their killer numbers | `journal/`, `graveyard.md` |

## The two pass tests (M6)

1. **Stranger-clone**: fresh clone + 15 minutes from `README.md` → a reproduced tearsheet whose
   headline number matches `WRITEUP.md`. Documented with a date.
2. **Recall**: three concepts explained from memory (no notes, no repo), one coded from scratch
   in an empty file. See [recall-test.md](recall-test.md).

## Automatic no-pass conditions

- Any quoted number that the repo cannot reproduce.
- Any strategy published without its graveyard line (dead or alive, every tested idea is listed).
- Live results presented without the reconciliation.
- A writeup whose caveat paragraph was written by someone else (or omitted).

## Self-assessment prompt (write the answers in your journal, not here)

1. Which single artifact would you defend hardest in an interview, and why?
2. Which part of the pipeline is most likely to be wrong in a way your tests would not catch?
3. If you had ten more weeks, what would you test first - and what would kill it?
