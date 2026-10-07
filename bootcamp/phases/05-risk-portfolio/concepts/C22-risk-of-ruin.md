---
id: C22
name: Risk of Ruin
tier: 4
phase: P5
week: 10
triggered_by: D15
trigger: Your "optimal" sizing has a 30% chance of halving the account before it compounds.
---

# 📐 CONCEPT: Risk of Ruin

**WHY NOW:** Kelly tells you the growth-optimal size; ruin arithmetic tells you whether the path there is survivable. Those are different questions, and the second is the one that ends accounts. Your Monte Carlo is about to show you a drawdown distribution - here is how to read it.

**FORMULA:** with continuous compounding and constant fractional exposure f, the expected time to lose a fraction a of capital is `t = ln(a) / (f·μ − f²σ²/2)`; more useful in practice: the probability of touching a drawdown level D before reaching a target gain G, approximated for a strategy with drift g and vol σ by the first-passage formula `P(hit D) ≈ ((G/D + 1)^(2g/σ²) − 1) / ((G/D + 1)^(2g/σ²) − 1 + ...)` - which is why the course makes you *simulate* it instead: simulation handles fat tails, autocorrelation and changing sizes, and the closed form does not.

**CODE:**

```python
import numpy as np
def ruin_prob(returns, dd_level=0.5, paths=2000, block=6, horizon=252, seed=11):
    rng, v, hits = np.random.default_rng(seed), returns.to_numpy(), 0
    for _ in range(paths):
        idx = np.concatenate([np.arange(s, s+block) % len(v) for s in rng.integers(0, len(v), horizon//block + 1)])[:horizon]
        curve = np.cumprod(1 + v[idx])
        if (curve / np.maximum.accumulate(curve)).min() <= -dd_level + 1e-12 or curve.min() <= 1 - dd_level:
            hits += 1
    return hits / paths
print(f"P(50% drawdown in 1 year) = {ruin_prob(portfolio_returns):.1%}")
```

**EXAMPLE:** At 3× leverage (full Kelly from C21), the simulation says P(50% drawdown within a year) = 34%. At 0.78× leverage (quarter-Kelly), it drops to 6% while keeping ~88% of the growth rate. Same strategy, same edge, one number different. This is why the risk policy needs a *de-risking rule with a resume condition*: at 0.78× you probably never trigger it, but the rule is the difference between a bad year and a terminal one - and it must be written before the drawdown, not during it.

**TIME:** 20 min.

**DONE WHEN:** You can simulate a drawdown probability under explicit sizing rules, explain in two sentences why "risk of ruin" is a property of the *rules plus the strategy* rather than of the strategy, and spot the wrong version - a ruin analysis that compounds raw strategy returns without applying the student's own leverage, or one that reports only the median path (see `RR1` in `python tools/spot_it_wrong.py`).
