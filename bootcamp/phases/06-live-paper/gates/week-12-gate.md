# Week 12 gate — milestone M5: Live paper

Run it: `make gate WEEK=12`.

**Checkpoint:** milestone M5 - 30+ days of live logs, a reconciliation report that attributes divergence to fees/slippage/timing/missed fills/regime, and a written expected-divergence budget for next month.

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G12.1 | `live/equity.csv` has 30+ rows | the 30-day window actually elapsed |
| G12.2 | `live/reconciliation.md` exists | the gap is documented |
| G12.3 | reconciliation mentions 2+ of slippage / fees / timing / missed | divergence is attributed, not described |
| G12.4 | `live/postmortem.md` exists | failures and interventions are recorded |
| G12.5 | 5+ journal entries dated in week 12 | the habit continues |
| G12.6 | *(manual)* M5 passed | milestone confirmation |

Confirm G12.6 with: `python tools/check_gate.py --week 12 --confirm G12.6`

## The M5 standard (verbatim from the registry)

> 30 days of live paper logs plus a reconciliation report; live vs backtest divergence explained.

"In the log" means a row per trading day with equity, and a JSON log per day with decisions -
including days the bot chose to do nothing. "Explained" means the component table sums to the
total gap, with any unexplained remainder explicitly quantified. A reconciliation that attributes
83% of the gap and says so is a pass; one that attributes 100% by relabelling the remainder
"market noise" is not.

## If it fails

- **Short of 30 days**: keep running into Week 13 and label the writeup "M5 in progress". Labeling honestly costs you nothing; backfilling equity rows costs you the whole course's credibility. (Also: this is why the clock starts in Week 5.)
- **Unexplained > 10%**: work the investigation list in `week-12.md` Tuesday. If it stays above 10%, publish it as a finding and state what data would close it.
- **Manual interventions found in the logs**: they belong in `postmortem.md` as killed variants, and the policy-trading claim restarts with a new window.
- **No expected-divergence budget**: write it. "Next month I expect live to trail the backtest by 8 bps/month: 3 bps fees, 2 bps timing, 3 bps structural slippage on the momentum leg." That sentence is the artifact that makes you a practitioner instead of a backtester.
