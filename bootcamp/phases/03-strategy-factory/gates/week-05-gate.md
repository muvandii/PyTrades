# Week 5 gate — you do not advance until this passes

Run it: `make gate WEEK=5`.

**Checkpoint:** three strategies with tearsheets, three verdicts, a populated `strategies/index.md`, at least two graveyard entries - and the live paper clock started (D0 is this week; the 30 days must run while you work).

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G5.1 | 3 verdict files (`strategies/S0[123]_*/verdict.md`) | three families, three conclusions |
| G5.2 | `strategies/index.md` exists | the registry is the track record |
| G5.3 | `graveyard.md` has 2+ entries | deaths are artifacts |
| G5.4 | `live/config.json` exists | the 30-day clock started in week 5, not week 12 |
| G5.5 | 5+ journal entries dated in week 5 | the habit continues |

## Manual checks

| id | confirm when you can |
| --- | --- |
| G5.6 | each verdict names the mechanism of death or survival in one sentence |

Confirm with: `python tools/check_gate.py --week 5 --confirm G5.6`

## On the live clock

The 30-day paper-trading window is graded in Week 12 and it needs 30 *real* days. Starting it in
Week 5 costs nothing (a config file and, from Week 11, a bot) and it means the reconciliation in
Week 12 has data that spans regimes instead of one quiet fortnight. Students who start the clock
in Week 11 fail M5 without exception; there is no way to compress a calendar.

## If it fails

- **Verdict files missing**: a strategy without a verdict is not tested - it is a notebook experiment. Write the verdict even when the answer is "inconclusive".
- **Registry empty**: fill in the numbers from the saved artifacts, not from memory. If a number is not in an artifact, re-run the backtest.
- **Graveyard thin**: you almost certainly had at least one death this week (usually S02 at 10-20 bps). If nothing died, your cost assumptions are too kind.
