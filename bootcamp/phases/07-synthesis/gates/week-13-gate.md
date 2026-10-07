# Week 13 gate — milestone M6: Capstone

Run it: `make gate WEEK=13`.

**Checkpoint:** milestone M6 - the stranger-clone test: a fresh clone plus a documented 15 minutes gets someone from README.md to a reproduced tearsheet; recall test passed (explain 3 concepts from memory, code 1 from scratch).

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G13.1 | 15+ `strategies/*/verdict.md` | the quarter's output is a track record, not a story |
| G13.2 | `WRITEUP.md` exists | the public writeup is the deliverable |
| G13.3 | `WRITEUP.md` contains a link (`http`) | it is published, not merely written |
| G13.4 | `PORTFOLIO.md` exists | the portfolio doc states what you would trade |
| G13.5 | `graveyard.md` has 5+ sections | the taxonomy is structured, one cause per section |
| G13.6 | 80+ journal entries across the course | the habit is the artifact that outlasts the course |
| G13.7 | *(manual)* stranger-clone test passed + recall test done (3 concepts explained, 1 coded from scratch) | the milestone's own standard |

Confirm G13.7 with: `python tools/check_gate.py --week 13 --confirm G13.7`

## The M6 standard

**Stranger-clone test.** A fresh `git clone` of the public repo, a timer, and 15 minutes: the
stranger runs the quickstart from `README.md` alone and reproduces a tearsheet whose headline
number matches the one `WRITEUP.md` quotes. Every friction you find is a bug in your
documentation, and the fix happens before you certify the pass.

**Recall test.** From [capstone/recall-test.md](../../../capstone/recall-test.md): explain three
concepts from memory (no notes, no repo) and code one from scratch in an empty file. The topics
are drawn from the course's core: annualisation, expectancy, drawdown, Sharpe, bootstrap CIs,
parameter plateaus, overfitting deflation, cointegration/half-life, vol targeting, Kelly/ruin,
slippage, reconciliation identity, regime splits.

## If it fails

- **Fewer than 15 verdicts**: count again - replications and live results count as verdicts if they have a verdict file. If you are genuinely short, you have one legitimate option: run the missing strategies this week and document them. Do not pad with un-run ideas.
- **Stranger-clone test failed on a fresh clone**: the fix is almost always a missing data step or an undocumented environment variable. Add the step to the README, re-clone, re-run. Document the fix, not just the pass.
- **No public link**: make the repo public and push. A local commit is not a publication; the course's final artifact is one a stranger can reach.
- **Recall test failed**: redo the concept immediately, in an empty file, then write two sentences about what the failure taught you. The recall test is diagnostic, not punitive - a gap found today is cheaper than the same gap in an interview or a live drawdown.
- **Graveyard not sectioned**: rewrite with one `##` heading per cause, ranked, each keeping its killer numbers. It is the artifact you will re-read before your next project.
