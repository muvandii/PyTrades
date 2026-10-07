# Verdict — S03_worked (Bollinger z-score reversion, tight threshold)

## The number

Net of 20 bps round-trip costs: **CAGR −1.67%, Sharpe −0.04, max drawdown −54.4% over 2,600 bars**.
Gross (0 bps): CAGR +6.15%, Sharpe 0.47. Out-of-sample half: Sharpe −0.37. Bootstrap 95% CI on
the OOS Sharpe: [−1.21, +0.44] — includes zero.

## The verdict

**No edge** (with a laboratory-data caveat: this is a mechanics demonstration, not market evidence).

## The mechanism

At a 5-day window with a −1.0σ entry trigger, the signal fires roughly weekly and turns over
38×/year. Its gross edge — a win-rate edge, 59.4% of trades — is worth about 15.7 bps of
round-trip cost, so anything above a very tight spread converts the same trades into losses. The
strategy did not fail because reversion is false; it failed because its *turnover* was matched to
a spread assumption it could never meet. The parameter sweep confirms it: lengthening the window
(→10) or loosening the trigger (→−1.5σ) cuts turnover and the net Sharpe crosses back above zero.

## Cost sensitivity and breakeven

| Round trip | 0 | 8 | 12 | **15.7** | 20 | 30 | 40 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CAGR | +6.2% | +3.0% | +1.4% | **0.0%** | −1.7% | −5.4% | −8.9% |
| Sharpe | 0.47 | 0.27 | 0.17 | **≈0.11** | −0.04 | −0.29 | −0.54 |

**Breakeven ≈ 15.7 bps.** For a liquid US equity ETF at retail spreads (5-15 bps round trip) this
is a coin flip at best; for anything with wider spreads it is dead on arrival.

## Fragility

- Turnover 38.2×/yr is not a parameter accident: shortening the window or tightening the trigger
  raises it further, and both changes make the net result worse.
- Parameter grid shows a *gradient*, not a cliff: every step toward patience (window 4→10,
  entry −0.8→−1.5) improves the net Sharpe. Death is predicted by turnover, visible before any
  optimization is attempted.
- The largest 5% of trades carry 95% of gross PnL — the gross edge is episode-driven, so even the
  zero-cost result was fragile.
- At a 2× cost assumption, CAGR −8.9%. No plausible universe makes this configuration work.

## Kill criteria (observable, so a stranger can check)

1. Net Sharpe < 0 at the assumed spread for two consecutive rolling years → stop.
2. Realised turnover > 30×/yr with round-trip spread > 15 bps → stop before starting.
3. OOS Sharpe CI includes zero *and* the point estimate is negative → no capital, regardless of
   the gross number.

## Graveyard line

Died of **cost death**. Killer number: breakeven ≈ 15.7 bps round trip against a 20 bps
assumption, at 38.2×/yr turnover. Entry filed: see `graveyard-entry.md`.
