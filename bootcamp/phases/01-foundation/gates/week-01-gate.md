# Week 1 gate — you do not advance until this passes

Run it: `make gate WEEK=1` (the runner reads `gates.json`, which was generated from the course registry).

**Checkpoint:** `make data && make validate` runs clean from a fresh clone; `reports/measurement-lab.md` contains an equity curve and an expectancy table computed from validated data.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G1.1 | 5+ instruments cached as CSVs in `data/` | the pipeline works end to end, not on one lucky file |
| G1.2 | `reports/data-validation.md` exists | validation was done, not assumed |
| G1.3 | `reports/measurement-lab.md` exists | the lab was written up |
| G1.4 | the lab report contains the word `expectancy` | the table exists, not just prose about the equity curve |
| G1.5 | 5+ journal entries dated in week 1 | the habit started on day one |
| G1.6 | the scaffold self-test command runs | your toolchain is wired correctly |

## Manual checks (the runner asks you to confirm these by name)

| id | confirm when you can |
| --- | --- |
| G1.7 | explain compounding and expectancy in two sentences each, and spot the wrong version of each in `python tools/spot_it_wrong.py --tier 1` |

Confirm with: `python tools/check_gate.py --week 1 --confirm G1.7`

## If it fails

- **No data**: `make data SYMBOLS="SPY QQQ" START=2010-01-01`. If the network is blocked, the course ships `sample-data/`; use it, and label any result as laboratory, not market.
- **Validation report missing**: run `make validate` and paste the output; do not summarise it from memory.
- **Journal too short**: backfill the days you actually worked, dated correctly. A gap is fine; a fake entry is not.
- **Cannot explain the concepts**: go back to Wed and Thu of week 1 and redo them with the notebook closed.
