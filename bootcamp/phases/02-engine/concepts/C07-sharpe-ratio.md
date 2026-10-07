---
id: C07
name: Sharpe Ratio
tier: 2
phase: P2
week: 3
triggered_by: D05
trigger: Two equity curves end at the same place and you cannot tell which one was luckier.
---

# 📐 CONCEPT: Sharpe Ratio

**WHY NOW:** Buy-and-hold and your strategy both returned about 8% a year, and you have to pick one. Sharpe answers "return per unit of wobble" in a single number - and it is the number every tearsheet, allocator and paper quotes, so you need to know exactly what it measures and what it ignores.

**FORMULA:** Sharpe = (annualised excess return) / (annualised volatility) = √ppy × mean(r − rf/ppy) / std(r − rf/ppy).

**CODE:**

```python
import numpy as np
def sharpe(returns, rf_annual=0.0, ppy=252):
    excess = returns - rf_annual / ppy
    sd = excess.std(ddof=1)
    return 0.0 if sd < 1e-12 else float(np.sqrt(ppy) * excess.mean() / sd)
print(round(sharpe(equity.pct_change().dropna()), 2))
```

**EXAMPLE:** Strategy A: +9%/yr with 18% vol → Sharpe 0.50. Strategy B: +7%/yr with 9% vol → Sharpe 0.78. B is the better risk-adjusted result, and it will usually be the better live experience too, because it is easier to size up without blowing up. Note what Sharpe does not see: A's one 30% month hurts a human more than the ratio suggests.

**TIME:** 20 min.

**DONE WHEN:** You can code Sharpe from memory, explain in two sentences what it normalises away (scale of exposure, frequency of measurement) and what it ignores (path, tails, autocorrelation), and spot the wrong version - a daily Sharpe multiplied by 12 instead of √252, or an annual risk-free rate subtracted from a daily mean (see `AN1` and `RF1` in `python tools/spot_it_wrong.py`).
