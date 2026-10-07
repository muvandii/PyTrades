# Week 10 gate — you do not advance until this passes

Run it: `make gate WEEK=10`.

**Checkpoint:** `reports/risk-policy.md` states the sizing rules in one page; the portfolio allocation beats equal-weight on the same signals; Monte Carlo shows your ruin probability under your own rules.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G10.1 | `reports/risk-policy.md` exists | the policy is a document, not an intention |
| G10.2 | `reports/portfolio-allocation.md` exists | the combination was measured, not assumed |
| G10.3 | `reports/monte-carlo.md` exists | survival analysis was actually run |
| G10.4 | `reports/regime-lab.md` exists | regimes were studied before they were used as excuses |
| G10.5 | 3+ `reports/sensitivity/*.csv` | sizing parameters were swept, not guessed |
| G10.6 | 5+ journal entries dated in week 10 | the habit continues |
| G10.7 | *(manual)* ruin probability computed, not assumed | an assumed risk figure is a wish |

Confirm G10.7 with: `python tools/check_gate.py --week 10 --confirm G10.7`

## The G10.7 standard

`reports/monte-carlo.md` must contain a number for P(50% drawdown within a year) *under the rules
written in the policy* — including de-risking. A simulation of raw strategy returns with no sizing
rules applied does not satisfy this check: that would be measuring a portfolio nobody is going to
trade.

## If it fails

- **Policy is three pages**: cut it to one. If a rule cannot be stated in one line, it is not a rule yet; it is a paragraph of intent.
- **Allocation does not beat equal-weight**: check the overlap period first (allocation computed over different windows is a common bug), then check whether your weights were fitted on the same data you evaluated on. If it still loses, document it — a documented loss is a pass; an undocumented "roughly similar" is not.
- **Monte Carlo shows ruin > 30%**: reduce target vol or add a de-risking rule, then re-run. This is the week's feedback loop, and it is supposed to change your policy.
