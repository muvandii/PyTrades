---
id: C24
name: Live vs Backtest Divergence
tier: 5
phase: P6
week: 12
triggered_by: D17
trigger: Live PnL is 40% below backtest PnL and you cannot tell which component ate it.
---

# 📐 CONCEPT: Live vs Backtest Divergence

**WHY NOW:** Your 30-day log is in and the gap is real: live is behind the shadow backtest by an amount that matters to your verdict. Before you blame the strategy, you need a taxonomy and sign conventions, because "the gap" is not one thing - it is six things that happen to sum to one number.

**FORMULA:** `live − backtest = −fees − slippage − timing − missed_fills + sizing_effects + regime + unexplained`. Keep signs consistent: a component that costs you money enters negatively, so the identity holds for any window. The check is arithmetic: components must sum to the total within rounding.

**CODE:**

```python
import pandas as pd
comp = pd.read_csv("live/reconciliation_components.csv")   # component, live_bps, backtest_bps
gap = (comp["live_bps"] - comp["backtest_bps"]).sum()
total = live_return_bps - backtest_return_bps
print(f"components sum to {gap:.1f} bps, observed total {total:.1f} bps, "
      f"unexplained {total - gap:.1f} bps ({(total - gap) / abs(total):.1%})")
assert abs(total - gap) < 0.10 * abs(total), "reconciliation does not add up - investigate, do not relabel"
```

**EXAMPLE:** Your gap is −46 bps over the window. Decomposition: −12 fees, −9 slippage, −18 timing (three days where your order went in after the open), −14 missed fills (two rejected orders never re-sent), +15 sizing (your risk policy ran smaller than the backtest's flat exposure), −8 regime (the window's realised vol was 1.4× the backtest median). Sum: −46. Unexplained: 0 bps. Nothing was "the market" - every basis point has a name, and two of the names (timing, missed fills) are fixable operations rather than costs of doing business.

**TIME:** 20 min.

**DONE WHEN:** You can decompose a live/backtest gap into the components with consistent signs and show the arithmetic adds up, explain in two sentences why a *sizing* difference can make live look better than the backtest without any advantage existing, and spot the wrong version - a reconciliation whose "unexplained" row is defined as whatever is left after the author rounded in their own favour (see `LV1` in `python tools/spot_it_wrong.py`).
