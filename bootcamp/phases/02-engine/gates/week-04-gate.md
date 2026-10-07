# Week 4 gate — milestone M2: Backtest engine

Run it: `make gate WEEK=4`.

**Checkpoint:** milestone M2 — hand yourself a fresh idea you have never tested and go from raw data to tearsheet + verdict in under 30 minutes, timed. Plus: walk-forward runner, tearsheets, and a green look-ahead suite.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G4.1 | `engine/walkforward.py` exists | OOS is a process, not a number |
| G4.2 | `tests/test_lookahead.py` exists | look-ahead discipline is code, not vibes |
| G4.3 | `python -m pytest tests -q` exits 0 | the suite is still green |
| G4.4 | 3+ `strategies/*/tearsheet.md` | the generator was actually used |
| G4.5 | `engine/README.md` mentions out-of-sample / OOS / walk-forward | the mechanism is documented |
| G4.6 | 5+ journal entries dated in week 4 | the habit continues |

## Manual checks

| id | confirm when you can |
| --- | --- |
| G4.7 | M2: a timed, documented run of a fresh idea from raw data to tearsheet + verdict in under 30 minutes |

Confirm with: `python tools/check_gate.py --week 4 --confirm G4.7`

## The M2 standard

- The idea must be new to you (not a re-run of Phase 1 work).
- The timer log must include the step breakdown, not just a total.
- "Under 30 minutes" means: spec written, signal implemented, backtest run, tearsheet generated, verdict written.
- One retry is normal. Two retries means the friction is structural: simplify the spec schema or the tearsheet before trying again - the engine is supposed to make you fast, not impressive.
