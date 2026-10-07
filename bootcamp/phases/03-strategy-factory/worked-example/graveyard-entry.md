# Graveyard entry — S03_worked (Bollinger z-score reversion, tight window)

## Identity

| Field | Value |
| --- | --- |
| Strategy id | `S03_worked` |
| Family | mean reversion (Bollinger / z-score) |
| Universe | `LAB_MR` (laboratory series) |
| Period | 2010-01-01 → 2019-12-19 (2,600 bars) |
| Spec fingerprint | see `reports/backtests/s03_worked_net20/meta.json` |
| Verdict date | 2026-10-07 |

## Cause of death

**Cost death** (taxonomy: `cost death`)

## The killer number

**Breakeven ≈ 15.7 bps round trip**, against a 20 bps assumption, at **turnover 38.2×/yr**.
Gross Sharpe 0.47 → net −0.04. Everything else about this strategy was fine: 197 trades is a
workable sample, the win rate (59.4%) is healthy, and the equity curve gross shows no look-ahead
signature.

## What was true before it died

The gross signal had a genuine (if small) statistical footprint on this series: Sharpe 0.47,
profit factor 1.26 — consistent with the lab series' planted reversion process. A student who
checked only the gross tearsheet would have written "small edge, worth watching".

## The lesson

**Turnover is a cost multiplier that is fully determined before any backtest runs.** The
turnover column (38.2×/yr) and the family's typical spread (5-15 bps round trip) were enough to
predict this death without running a single bar. From now on, check list: before running a new
specification, estimate `turnover × spread` and compare it to the gross edge you expect to find.

## Sister entry

The loose variant of the same signal (`window=20`, `entry_z=−2.0`, 8.3×/yr) survives the sweep:
Sharpe 0.54 → 0.31 from 0 to 30 bps. Same family, same data, one parameter decision — the
difference between a live strategy and a corpse here was patience, not insight.
