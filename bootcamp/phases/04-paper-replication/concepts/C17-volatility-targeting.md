---
id: C17
name: Volatility Targeting
tier: 3
phase: P4
week: 7
triggered_by: D12
trigger: Your TSMOM signal is right 55% of the time and its risk still swings 3× between regimes.
---

# 📐 CONCEPT: Volatility Targeting

**WHY NOW:** Your raw TSMOM returns are dominated by two or three turbulent months; in calm periods the same signal earns almost nothing because the positions are small in dollar-risk terms. Position sizing by *recent volatility* - not by conviction - is the standard fix, and it is also the object of study in Week 9.

**FORMULA:** w_t = (target_vol / σ_t) × signal_t, with σ_t a trailing estimate (e.g. 60-day EWMA) of annualised return volatility; cap and floor the multiplier. Realised vol is annualised as `std(r) × √252`.

**CODE:**

```python
import numpy as np, pandas as pd
r = prices.pct_change()
sigma = (r.ewm(span=60, min_periods=60).std() * np.sqrt(252)).shift(1)   # trailing, never contemporaneous
multiplier = (0.10 / sigma).clip(upper=3.0)                              # cap the leverage
positions = signal * multiplier
print(multiplier.mean().round(2), "cap binds", float((multiplier >= 3.0).mean().round(3)))
```

**EXAMPLE:** Your TSMOM book: in the 2017 calm, σ = 6% and the multiplier is 1.67; in March 2020, σ = 45% and the multiplier floors at ~0.22. Same signal, third of the risk. Result on your tearsheet: vol drops from 15% to 11%, CAGR moves from 6.1% to 5.8% - Sharpe up, return slightly down, which is exactly the trade the paper documents. Note the two traps: `.shift(1)` (a contemporaneous σ is a look-ahead) and the cost of the multiplier changing every day.

**TIME:** 20 min.

**DONE WHEN:** You can code a causal vol target with a cap, explain in two sentences why vol scaling can raise Sharpe without predicting returns, and spot the wrong version - a σ computed from the same bar's return, or a target that is never capped (see `VT1` in `python tools/spot_it_wrong.py`).
