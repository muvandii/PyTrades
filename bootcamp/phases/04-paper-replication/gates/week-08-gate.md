# Week 8 gate — you do not advance until this passes

Run it: `make gate WEEK=8`.

**Checkpoint:** `papers/R2_pairs/comparison.md` includes the cointegration test output, the chosen pair(s), the spread z-score rules, and a walk-forward run where the pair was selected only on training data.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G8.1 | `papers/R2_pairs/impl.py` exists | the implementation is the artifact |
| G8.2 | `comparison.md` mentions coint / ADF / half-life / z-score | the *test* is part of the deliverable |
| G8.3 | `papers/R2_pairs/deviations.md` exists | deviations logged |
| G8.4 | 5+ journal entries dated in week 8 | the habit continues |
| G8.5 | *(manual)* pair selection happened on training data only | the whole point of the week |

Confirm G8.5 with: `python tools/check_gate.py --week 8 --confirm G8.5`

## The G8.5 standard

For each pair you traded, you must be able to state the formation window's end date and show that
no selection decision used data after it. The honest failure mode here is worth stating plainly:
if you looked at the second half of the sample while choosing pairs, the correct action is to say
so in `deviations.md`, re-select on the training half, and report both Sharpes. A disclosed
look-ahead is a finding; an undisclosed one voids the deliverable.

## If it fails

- **No test output**: run `coint` (Engle-Granger) and the half-life regression for each pair and paste the table. A pair without a test is a guess with two tickers.
- **Selection used the full sample**: re-select; expect Sharpe to drop. That drop *is* the week's most valuable number — it is the size of the look-ahead in Sharpe units.
- **No break stop**: add `|z| ≥ 3.5` before re-running. Compare the trade distribution; one merger-adjacent pair usually explains the difference.
- **Costs missing on the short leg**: charge four spreads per round trip and re-run; pairs strategies live or die on exactly this line.
