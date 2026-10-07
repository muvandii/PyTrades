# Week 7 gate — you do not advance until this passes

Run it: `make gate WEEK=7`.

**Checkpoint:** `papers/R1_tsmom/comparison.md` shows your Sharpe and the paper's side by side, with every gap traced to a named deviation (universe, period, vol scaling, costs).

## Automated checks

| id | what it checks | why it matters |
| --- | --- | --- |
| G7.1 | `papers/R1_tsmom/impl.py` exists | the replication is code, not a book report |
| G7.2 | `papers/R1_tsmom/comparison.md` exists | the results-vs-claims table is the deliverable |
| G7.3 | `papers/R1_tsmom/deviations.md` exists | deviations are logged, not remembered |
| G7.4 | 5+ journal entries dated in week 7 | the habit continues |
| G7.5 | *(manual)* every gap to the paper is traced to a named deviation | a gap without a cause is an excuse |

Confirm G7.5 with: `python tools/check_gate.py --week 7 --confirm G7.5`

## What "every gap traced" means in practice

The comparison table has rows for Sharpe, vol, max drawdown, turnover and sample. Each row in
which your number differs from the paper's needs a *cause from the taxonomy* (universe, period,
costs, sizing, data frequency, excess-return definition), not a vibe. Two examples of acceptable
answers:

- "Sharpe 0.62 vs 1.00 gross: universe deviation — ETFs cannot express commodity and FX trends;
  the mechanism needs many weakly correlated markets."
- "Max DD −28% vs −12%: sizing deviation — my leverage cap of 1.0 prevents the vol scaler from
  cutting exposure as aggressively as the paper's target allows."

And one unacceptable answer: "different market conditions".

## If it fails

- **No comparison table**: re-read the dossier's "what a replication owes the reader" section and build the table *before* running anything.
- **Deviations.md is empty**: start with the three deviations the dossier already predicts (universe, period, costs) and measure each one by re-running with that single change.
- **G7.5 cannot be confirmed**: name the largest gap and chase it with a re-run. If it will not move, the deviation class is probably "sizing" or "universe" and you can state its direction without perfect precision - say "direction: negative, rough size: 0.2-0.4 Sharpe" and move on.
