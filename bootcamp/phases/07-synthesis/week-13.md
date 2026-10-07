---
week: 13
phase: P7
title: Ship It in Public
deliverables: [D18]
concepts: []
milestone: M6
hours: 14-20
---

# Week 13 — Ship It in Public

## Learning objective

Publish the portfolio, the graveyard and the writeup so a stranger can clone your repo, run it, and understand the whole thing in fifteen minutes - and pass the recall test: three concepts explained from memory, one coded from scratch.

## Deliverable

- [D18 — Capstone: public repo + writeup + portfolio doc + roadmap](deliverables/D18.md): `README.md`, `WRITEUP.md`, `PORTFOLIO.md`, `graveyard.md` (taxonomy), all in a public repo.

## Daily tasks

### Mon — Close the graveyard with a taxonomy

1. Open every entry in `graveyard.md` and re-read the cause. Cluster them into 3-5 categories (the taxonomy from `shared/templates/graveyard-entry.md` gives you the vocabulary; your data gives you the ranks).
2. Write the ranked list at the top of the file: cause, count, share, and the *predictive signal* for each (e.g. "cost death: 9 of 22; predicted by turnover > 20×/yr before any backtest ran").
3. Require the gate's structure: 5+ `##` sections in the file, each a cause with its entries beneath.

*Time: 3-4 h. This ranked list is, as the registry says, the most valuable artifact you built this quarter.*

### Tue — Write `WRITEUP.md`

Use [capstone/writeup-template.md](../../capstone/writeup-template.md). One page, in this order:

1. **The question** you actually answered this quarter (not "I learned Python").
2. **The method**: your engine, your costs, your OOS discipline, your live window - in five lines.
3. **The three best artifacts**: links to the tearsheet that matters, the reconciliation that surprised you, the graveyard taxonomy.
4. **The three most instructive deaths**: what died, of what, and what you do differently now.
5. **The honest limitation**: the largest caveat a hostile reader would raise, stated by you first.
6. **What is next**: two or three concrete next experiments, each with a kill criterion.

*Time: 3-4 h.*

### Wed — Publish the repo

1. `README.md` at the repo root, structured for a stranger in fifteen minutes to get from clone to a reproduced tearsheet:
   - what this is, in two sentences;
   - the 4-command quickstart (`make data`, `make run`, `make tearsheet`, `make test`), each command verified on a **fresh clone**;
   - where the artifacts live (backs_test results, tearsheets, verdicts, graveyard, live logs);
   - what a stranger needs to reproduce the headline number, including the data source and its limitations;
   - the link to `WRITEUP.md` and a one-line summary of the honest limitation.
2. Make the repository public. Verify that the clone is clean of anything you would not want read (keys, personal notes).
3. Record the public URL; it goes into the gate's link check and the writeup.

*Time: 4-5 h.*

### Thu — `PORTFOLIO.md` and the roadmap

1. `PORTFOLIO.md` from [capstone/portfolio-template.md](../../capstone/portfolio-template.md): the current portfolio (strategies, weights, sizing rules), the evidence behind each line, the risk policy in one paragraph, the live window's status, and what would make you remove a line.
2. Roadmap: three experiments for next quarter - each with a hypothesis, a kill criterion, and the artifact it would produce. An experiment without a kill criterion is a hobby; write the criterion first.
3. Refresh `strategies/index.md` one last time: it is the portfolio's evidence table.

*Time: 3-4 h.*

### Fri — The stranger-clone test (the milestone)

1. Clone your repo into a fresh directory (`git clone <public-url> /tmp/stranger-test`), and give a friend - or a timer and disciplined ignorance - 15 minutes starting from the README.
2. The test passes if: `make data && make run && make tearsheet` reproduces a tearsheet whose headline number matches the one your writeup quotes, without reading anything outside the README.
3. Fix every friction you find (missing step, unstated environment variable, data path assumption) and re-run the test. Record the pass in `README.md` ("stranger-clone test: passed YYYY-MM-DD, fresh clone, 15 min").

*Time: 4-5 h including fixes.*

### Sat — The recall test

1. From [capstone/recall-test.md](../../capstone/recall-test.md): explain three concepts from memory, out loud or in writing, without notes. Suggested sample: annualisation and its traps; bootstrap CIs and their blocks; the reconciliation's component identity.
2. Code one of them from scratch in an empty file: no imports from your repo, no copy-paste. Suggested: max drawdown + duration, or a block bootstrap CI for Sharpe.
3. Score yourself honestly against the rubric in the recall test, and redo any fail on the spot - the point is the gap, not the grade.

*Time: 3-4 h.*

### Sun — Final gate, retro, and the last journal entry

1. `make gate WEEK=13`: 15+ verdicts, WRITEUP.md with a public link, PORTFOLIO.md, the graveyard taxonomy, 80+ journal entries.
2. Confirm M6 (manual check G13.7): the stranger-clone test passed *and* the recall test done.
3. Write the final journal entry: the three things you now believe about markets that you did not believe in Week 1, and the one you still cannot test. Keep it; it is the seed of the next quarter.

*Time: 3-4 h.*

## Gate

`make gate WEEK=13` - see [gates/week-13-gate.md](gates/week-13-gate.md). **Milestone M6:** the stranger-clone test - a fresh clone plus a documented 15 minutes gets someone from README.md to a reproduced tearsheet; recall test passed (explain 3 concepts from memory, code 1 from scratch).

## Graveyard prompt

Close the graveyard with a taxonomy: cluster all deaths into 3-5 causes and rank them. That ranked list is the most valuable artifact you built this quarter - it is the compressed form of everything the market taught you, and it is the thing a future reader will quote back at you. Every entry keeps its killer number; every cause keeps its predictive signal.
