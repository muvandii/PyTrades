# Reconciliation: live paper vs backtest

> The Week 12 deliverable. Goal: explain every basis point of the gap, and leave
> behind a number you can predict next month.

## 1. The two lines

| | Backtest (same window) | Live paper | Gap |
| --- | --- | --- | --- |
| Total return | | | |
| Sharpe (annualised) | | | |
| Max drawdown | | | |
| Turnover | | | |
| Trades | | | |

Backtest window matched to live days: `<start>` → `<end>`, using
`result.state_at(date)` for the engine's intended positions each day.

## 2. Attribution (the actual work)

Estimate first, measure second.

| Bucket | Expected | Measured | Method |
| --- | --- | --- | --- |
| Fees | | | sum of commissions from fills |
| Slippage | | | (fill price - decision price) × side, per order |
| Timing (open vs close fills) | | | re-run backtest with live fill assumptions |
| Missed / skipped signals | | | compare daily intended vs submitted orders |
| Partial fills / sizing drift | | | |
| Data differences (adjusted vs raw) | | | |
| Regime | | | live window vs backtest regime distribution |

**Unexplained residual:** __% (if this is more than 30% of the gap, hunt harder)

## 3. Divergence budget for next month

Predicted: fees __ · slippage __ · timing __ · missed fills __ · total drag __ bps/month.

## 4. What I changed in the live rules (and when)

| Date | Change | Reason | Days affected |
| --- | --- | --- | --- |
<undisclosed mid-run changes invalidate the experiment - log them all>
