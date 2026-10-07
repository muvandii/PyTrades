---
id: C10
name: Transaction Costs & Slippage
tier: 2
phase: P2
week: 4
triggered_by: D06
trigger: Your strategy is beautiful with zero costs and dead at 10 bps round-trip.
---

# 📐 CONCEPT: Transaction Costs & Slippage

**WHY NOW:** Your momentum rule made 14% a year gross and 3% net. Before you conclude the strategy is bad, you need to know how costs work, because the answer decides whether you should change the strategy or the venue.

**FORMULA:** cost_per_bar = Σ|Δweight| × (fee_bps + slippage_bps) / 10_000; annual drag ≈ turnover_annual × cost_bps; breakeven is where CAGR crosses zero.

**CODE:**

```python
from kit import spine as spine_mod
grid = spine_mod.cost_breakeven("S01_ma_cross")     # 0..30 bps, CAGR/Sharpe/MaxDD per level
print(grid.to_string(index=False))
print("breakeven:", grid.loc[grid["cagr"].lt(0).idxmax(), "fee_bps_roundtrip"] if grid["cagr"].lt(0).any() else "> 30 bps")
```

**EXAMPLE:** `S01_ma_cross` turns over 0.46% per day ≈ 1.15× per year. At 10 bps round trip that is ~0.12% a year of drag - irrelevant. Your daily z-score reversion idea, however, turns over 6× per year: same 10 bps is 6% a year, which is more than its whole gross edge. Same cost, two completely different verdicts, decided by a property of the *signal*.

**TIME:** 20 min.

**DONE WHEN:** You can code a cost function, explain in two sentences why turnover (not trade count) is the right denominator for costs, and spot the wrong version - a constant per-bar cost that ignores turnover, or a backtest that optimises gross and reports net (see `CO1` in `python tools/spot_it_wrong.py`).
