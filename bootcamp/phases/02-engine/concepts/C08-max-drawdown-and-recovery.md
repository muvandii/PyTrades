---
id: C08
name: Max Drawdown & Recovery
tier: 2
phase: P2
week: 4
triggered_by: D07
trigger: Your first engine tearsheet prints a 47% drawdown and you nearly delete the strategy.
---

# 📐 CONCEPT: Max Drawdown & Recovery

**WHY NOW:** Your engine just printed a 47% peak-to-trough decline. Sharpe says the strategy is fine; your stomach says otherwise. Both are right: Sharpe measures the average wobble, drawdown measures the worst one - and the worst one is what decides whether you keep trading.

**FORMULA:** drawdown_t = equity_t / cummax(equity)_t − 1; max drawdown = min(drawdown); duration = longest run below a previous peak; recovery = bars from trough back to the old peak.

**CODE:**

```python
from kit import metrics as m
dd = m.drawdown_series(equity)
print(f"maxDD {m.max_drawdown(equity):.1%}  duration {m.max_drawdown_duration(equity)} bars")
print(f"recovery {m.time_to_recovery(equity)} bars (0 = not recovered in sample)")
print(f"ulcer (RMS drawdown) {m.ulcer_index(equity):.2%}")
```

**EXAMPLE:** Your trend strategy: maxDD 47%, duration 1,240 bars, recovered after 1,410 bars. In calendar terms that is three and a half years underwater. A 6-year backtest that contains a 3.5-year recovery is really a 2.5-year backtest plus one long apology - the drawdown numbers change what the sample can claim.

**TIME:** 20 min.

**DONE WHEN:** You can code max drawdown, duration and recovery from an equity curve, explain in two sentences why drawdown and Sharpe can disagree so violently (path and tails), and spot the wrong version - computing max drawdown as the worst single return instead of peak-to-trough equity (the `DD1` snippet in `python tools/spot_it_wrong.py`).
