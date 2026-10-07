# Week 3 gate — you do not advance until this passes

Run it: `make gate WEEK=3`.

**Checkpoint:** your engine passes the 8 engine unit tests and the time-travel test (positions up to T are identical whether or not future data exists), and reproduces buy-and-hold within 1% of the raw price return on SPY.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G3.1 | `engine/backtest.py` exists | the deliverable is a file, not a plan |
| G3.2 | `python -m pytest tests -q` exits 0 | engine work is tested work |
| G3.3 | `reports/cost-sensitivity.md` exists | costs were measured, not assumed |
| G3.4 | `engine/costs.py` exists | costs live in the engine, not in the report |
| G3.5 | `engine/README.md` exists | every engine change must be documented |
| G3.6 | 5+ journal entries dated in week 3 | the habit continues |

## Manual checks

| id | confirm when you can |
| --- | --- |
| G3.7 | buy-and-hold reproduces within 1%, and the time-travel test passes against your engine |

Confirm with: `python tools/check_gate.py --week 3 --confirm G3.7`

## If it fails

- **Tests failing on the contract suite**: run one failure at a time; the first is usually the execution lag (`signal[t]` applied to bar `t`). Fix the shift before anything else.
- **Buy-and-hold off by more than 1%**: you are probably compounding weights instead of quantities, or charging costs that a passive position should not pay (a constant weight only pays on entry).
- **Cost report missing**: `make costs S=<id>` produces the grid; paste the table and the breakeven.
