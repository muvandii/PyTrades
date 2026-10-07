# Week 6 gate — milestone M3: Strategy factory

Run it: `make gate WEEK=6`.

**Checkpoint:** milestone M3 - six strategies tested, 3+ in the graveyard, at least one survivor whose OOS Sharpe sits inside a bootstrap CI that excludes zero.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G6.1 | 6+ verdict files | the factory ran at volume |
| G6.2 | `graveyard.md` has 3+ entries | failures are the majority by design |
| G6.3 | `reports/overfitting-audit.md` exists | the mirror was looked into |
| G6.4 | 2+ sensitivity CSVs | parameter fragility was measured, not asserted |
| G6.5 | `reports/bootstrap.md` contains confidence/CI/percentile language | the CI was computed |
| G6.6 | 5+ journal entries dated in week 6 | the habit continues |

## Manual checks

| id | confirm when you can |
| --- | --- |
| G6.7 | M3: at least one survivor whose OOS Sharpe CI excludes zero - or a documented statement that none do, with six verdicts as evidence |

Confirm with: `python tools/check_gate.py --week 6 --confirm G6.7`

## Honest failure is a pass

If all six strategies died, M3 can still pass with the second branch of the pass condition:
"or an honest statement that none do, with the graveyard to prove you tested". The course grades
the process, not the market's cooperation. What does *not* pass: a survivor whose CI includes
zero presented as an edge, or a CI that was never computed.

## If it fails

- **Fewer than 6 verdicts**: run the remaining families even if you expect them to fail. Expected failure is data.
- **Audit missing sections**: the seven questions are the deliverable. Answer "unknown" where you truly do not know, and say what you would need to find out.
- **CI excludes zero by construction**: check your bootstrap resamples *returns* (not trades), uses a block length at least as long as the holding period, and does not re-centre the distribution.
