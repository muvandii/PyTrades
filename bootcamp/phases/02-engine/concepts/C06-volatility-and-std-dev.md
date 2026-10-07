---
id: C06
name: Volatility & Standard Deviation
tier: 2
phase: P2
week: 3
triggered_by: D05
trigger: You want to compare a 1.2%/day strategy to a 0.4%/day strategy and know if that is a lot.
---

# 📐 CONCEPT: Volatility & Standard Deviation

**WHY NOW:** Two strategies produce returns. One moves 1.2% a day, the other 0.4%. You suspect the first is riskier, but "riskier" is not a number, and you cannot compare their returns until you have a denominator for risk. Standard deviation of returns is that denominator.

**FORMULA:** vol_annual = std(returns, ddof=1) × √periods_per_year; you need the sample standard deviation (ddof=1), not the population one, because you are estimating, not describing.

**CODE:**

```python
import numpy as np
r = equity.pct_change().dropna()
vol_ann = r.std(ddof=1) * np.sqrt(252)
print(f"daily vol {r.std(ddof=1):.3%} -> annual vol {vol_ann:.2%}")
# sanity anchor: SPY daily vol ~1.0-1.2% -> annual ~16-19%
```

**EXAMPLE:** Your trend strategy shows daily vol 0.9% (≈14.3% annual) against the market's 1.1% (≈17.5%): slightly calmer, so a comparison of raw returns now has context. And it exposes the real driver: the strategy is out of the market 40% of days, so its low vol is partly just less exposure - a fact that will matter in Week 10 when you size positions.

**TIME:** 20 min.

**DONE WHEN:** You can code annualised vol with the right ddof, explain in two sentences why volatility (not drawdown) is the standard risk unit in portfolio maths, and spot the wrong version - a "risk-adjusted" comparison that uses raw returns without any volatility normalisation, or a std computed with ddof=0 on a tiny sample (see `AN1` in `python tools/spot_it_wrong.py`).
