# Week 2 gate — milestone M1: Reality check

Run it: `make gate WEEK=2`.

**Checkpoint:** milestone M1 — a timed, unassisted 30-minute debunk, start to written verdict, with the timer log kept in the report. Also: three debunk files, three graveyard entries, validation from Week 1 still green.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G2.1 | 3+ files matching `reports/debunks/debunk-*.md` | three claims, not one lucky debunk |
| G2.2 | `debunk-01.md` contains `elapsed` or `minutes` or `timer` | M1 is about speed: the time must be recorded |
| G2.3 | `graveyard.md` has 3+ entries | deaths are logged as artifacts |
| G2.4 | 5+ journal entries dated in week 2 | the habit continued |

## Manual checks

| id | confirm when you can |
| --- | --- |
| G2.5 | M1: you have demonstrably debunked a fresh viral claim in 30 timed minutes - the timer log is in `debunk-01.md` |

Confirm with: `python tools/check_gate.py --week 2 --confirm G2.5`

## Notes on the timed debunk

- The 30 minutes covers **reconstruction through verdict**. You may re-read the claim beforehand; you may not pre-run the code.
- If you overran, the milestone is still failed this week - but the retry is cheap: do a fourth claim cold. Most students need two attempts; the second is usually 20 minutes.
- "Debunked" is not the only passing outcome. A claim that survives all three checks with the checks documented is a passing M1.
