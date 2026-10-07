---
id: C21
name: Kelly & Fractional Kelly
tier: 4
phase: P5
week: 10
triggered_by: D15
trigger: You have an edge and no idea what fraction of your capital it deserves.
---

# 📐 CONCEPT: Kelly & Fractional Kelly

**WHY NOW:** Your portfolio has an edge; the sizing question is no longer "should I trade?" but "how much?". Full Kelly maximises long-run growth, and its drawdowns are deeper than anyone's tolerance - so you will trade a fraction of it. Knowing the fraction's meaning is what keeps the choice from being arbitrary.

**FORMULA:** continuous Kelly: `f* = μ / σ²` (fraction of capital, using excess return); discrete Kelly: `f* = (p·b − q)/b` where p is win probability, q = 1 − p, b is win/loss ratio; growth rate at fraction k of Kelly is `g(k) = k(1 − k/2)·g*`. Drawdown scales roughly linearly with k, which is the whole reason quarter-Kelly is popular: 75% of the growth for a quarter of the drawdown.

**CODE:**

```python
import numpy as np
def kelly(mu_annual, vol_annual, rf=0.0):
    return (mu_annual - rf) / vol_annual**2
f = kelly(0.08, 0.16); print(f"full Kelly {f:.2f}x, half {f/2:.2f}x, quarter {f/4:.2f}x")
for k in (0.25, 0.5, 1.0, 1.5):
    print(f"  {k:.2f} Kelly: growth {k*(1-k/2):.0%} of max")
```

**EXAMPLE:** Your portfolio: excess return 8%, vol 16% → full Kelly 3.1× leverage, which is what the formula says to run with a Sharpe 0.5 strategy. That is obviously wrong for a student with a 30% drawdown tolerance, and it tells you something important: **Kelly assumes your μ and σ are exactly right, forever.** With estimation error, the growth-optimal fraction shrinks - and with a fat-tailed strategy, the drawdown at full Kelly is brutal in ways the formula's clean parabola does not show. Quarter-Kelly (0.78×) gives 88% of the growth with a quarter of the drawdown, which is why it is the course's default recommendation for a first live deployment.

**TIME:** 20 min.

**DONE WHEN:** You can compute continuous and discrete Kelly, state the growth-vs-fraction relationship, explain in two sentences why estimation error argues for a fraction of Kelly rather than full Kelly, and spot the wrong version - sizing at full Kelly on an estimated μ, or applying Kelly to a strategy whose win/loss distribution is not what the formula's b assumes (see `KL1` in `python tools/spot_it_wrong.py`).
