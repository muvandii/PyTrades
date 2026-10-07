# Week 9 gate — milestone M4: Paper replication

Run it: `make gate WEEK=9`.

**Checkpoint:** milestone M4 — 2-3 replications shipped, each with `comparison.md` + `deviations.md`, plus `papers/synthesis.md` answering what replicated, what did not, and why.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G9.1 | `papers/R3_volmanaged/impl.py` exists | the third replication is real |
| G9.2 | 3+ `papers/R*/comparison.md` | all three replications compared to their papers |
| G9.3 | `papers/synthesis.md` exists | the cross-paper answer is the phase's payoff |
| G9.4 | 5+ journal entries dated in week 9 | the habit continues |
| G9.5 | `reports/retro-P4.md` answers the 3 retro questions | phase retros are graded artifacts |
| G9.6 | *(manual)* M4 passed | milestone confirmation |

Confirm G9.6 with: `python tools/check_gate.py --week 9 --confirm G9.6`

## The M4 standard

- Each replication has all three artifacts (implementation, comparison, deviation log) - R3's
  deviations live inside its `comparison.md` if you prefer, but the gap analysis must be there.
- Every compared number traces to a saved backtest with `meta.json` fingerprints.
- `synthesis.md` contains a *mechanism-level* sentence per replication and one rule you will apply
  to the next paper. A summary of the three weeks is not a synthesis.

## If it fails

- **Only two replications**: still passes M4 (the registry says 2-3), but if the missing one is R2, you have skipped cointegration and the look-ahead measurement - the most valuable part of the phase. Do R2 in Week 10's slack time and note it in the journal.
- **Synthesis is a summary**: rewrite with the four questions as headings; one paragraph each, mechanism first.
- **Retro missing**: it is three questions from `shared/retro-template.md`; ten minutes of writing, and it feeds your Week 13 writeup.
