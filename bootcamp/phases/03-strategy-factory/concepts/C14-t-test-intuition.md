---
id: C14
name: t-test Intuition
tier: 3
phase: P3
week: 6
triggered_by: D10
trigger: Your strategy earns +0.031% per day and you cannot tell whether that is signal or noise.
---

# 📐 CONCEPT: t-test Intuition

**WHY NOW:** +0.031% per day sounds like something (it annualises to ~8%). Before you write a verdict on it, you need to know whether a mean return that size could plausibly come from a coin flip on this sample - and that is exactly what a t-statistic measures.

**FORMULA:** t = mean(r) / (std(r) / √n); in return terms, t ≈ Sharpe × √years. Rule of thumb: |t| > 2 is "hard to explain by luck", |t| > 3 is "worth defending", and the *clinical* bar for a daily equity strategy is nearer 3 because you looked at many strategies.

**CODE:**

```python
import numpy as np
r = oos_returns.dropna()
t = r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))
print(f"mean {r.mean():.4%}/day, n {len(r)}, t = {t:.2f}")
print(f"implied by Sharpe: {sharpe(r) * np.sqrt(len(r)/252):.2f}  (same number, different route)")
```

**EXAMPLE:** Your survivor: mean +0.031%/day, std 0.84%, n = 756 → t = 1.02. That is a coin flip, dressed as an 8% annual return. And the trap: the t-stat assumes 756 *independent* bets, but a strategy holding a position for 6 days has ~126 independent episodes, so the honest t is nearer 1.02 × √(126/756) ≈ 0.42. **The independent-bet count is the number most students never compute, and it is the one that decides most verdicts.**

**TIME:** 20 min.

**DONE WHEN:** You can compute a t-stat and convert it to/from Sharpe, explain in two sentences why autocorrelated position holding inflates t, and spot the wrong version - a t-stat computed on daily returns of a strategy whose positions persist for weeks, reported without mentioning the effective sample size (see `TT1` in `python tools/spot_it_wrong.py`).
