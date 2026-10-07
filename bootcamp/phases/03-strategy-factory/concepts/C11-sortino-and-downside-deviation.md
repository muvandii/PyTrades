---
id: C11
name: Sortino & Downside Deviation
tier: 2
phase: P3
week: 5
triggered_by: D08
trigger: Your reversion strategy has a Sharpe near zero but its losing months look small - and its wins look lumpy.
---

# 📐 CONCEPT: Sortino & Downside Deviation

**WHY NOW:** S02's Sharpe sits at 0.1 and you are ready to bury it - but when you look at the losses they are frequent and small, while the profits arrive in a few big jumps. Sharpe punishes those jumps (it counts upside moves as "risk"); your actual lived experience of the strategy is different. You need a ratio that only counts the pain.

**FORMULA:** downside deviation = std of returns below a target (usually 0 or the risk-free rate); Sortino = (annualised excess return) / (annualised downside deviation). Upside volatility is not in the denominator.

**CODE:**

```python
import numpy as np
def sortino(returns, target=0.0, ppy=252):
    downside = (returns - target / ppy).clip(upper=0.0)
    dd = np.sqrt((downside ** 2).mean()) * np.sqrt(ppy)
    return 0.0 if dd < 1e-12 else float((returns.mean() - target / ppy) * ppy / dd)
print(round(sortino(equity.pct_change().dropna()), 2))
```

**EXAMPLE:** S02's numbers: Sharpe 0.10, Sortino 0.62. The gap is entirely upside variance - the strategy's good days are big and rare. That is a *positive* signature for a reversion strategy, and it changes the question from "is there an edge?" to "how many losing days can I survive waiting for the payoff?" Both numbers belong in the tearsheet; a mid-morning decision on a Tuesday belongs to the Sortino.

**TIME:** 20 min.

**DONE WHEN:** You can code Sortino with the downside-only denominator, explain in two sentences why a strategy with lumpy gains and steady small losses can look bad on Sharpe and fine on Sortino, and spot the wrong version - a "Sortino" computed with the standard deviation of all returns (the `SO1` snippet in `python tools/spot_it_wrong.py`).
