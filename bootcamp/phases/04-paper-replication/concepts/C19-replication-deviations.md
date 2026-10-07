---
id: C19
name: "Replication Deviations: Statistical vs Economic Significance"
tier: 3
phase: P4
week: 9
triggered_by: D14
trigger: Your replication of the paper returns 60% of the paper's Sharpe and you must decide whether that counts as replicated.
---

# 📐 CONCEPT: "Replication Deviations: Statistical vs Economic Significance"

**WHY NOW:** Three replications, three results, none of them matching the paper exactly. You need a way to say "this replicated" or "this did not" that is not a feeling about the size of a number, and you need to separate "is this a real difference?" from "does this difference matter?"

**FORMULA:** statistical significance asks whether the observed difference could plausibly arise under the null: use a CI or test on the *difference* (bootstrap the difference directly, or use `ΔSharpe / SE(ΔSharpe)`; SE ≈ `√(SE₁² + SE₂²)` when the two runs share no data, and much smaller when they do). Economic significance asks whether it changes a decision: bps per year, capacity, cost to implement, drawdown path.

**CODE:**

```python
import numpy as np
def sharpe_ci(r, n=2000, block=6, seed=7):
    rng, v, L, out = np.random.default_rng(seed), r.to_numpy(), block, []
    for _ in range(n):
        idx = np.concatenate([np.arange(s, s+L) % len(v) for s in rng.integers(0, len(v), len(v)//L+1)])[:len(v)]
        s = v[idx]; sd = s.std(ddof=1)
        out.append(0.0 if sd == 0 else np.sqrt(252)*s.mean()/sd)
    return np.percentile(out, [2.5, 97.5])
print("paper-side CI", np.round(sharpe_ci(r_paper_like), 2), " mine", np.round(sharpe_ci(r_mine), 2))
```

**EXAMPLE:** You replicate Moreira-Muir: your Sharpe improvement is +0.15 with a 95% CI of [−0.06, +0.36]. Statistically: indistinguishable from zero on your sample - you cannot claim the effect exists, nor that it does not. Economically, meanwhile: the improvement requires +120% annual turnover and a leverage facility, and it is concentrated in two assets. The honest verdict sentence reads: "the direction is consistent with the paper, but on this sample and universe the effect is neither statistically resolvable nor economically attractive net of costs" - two separate findings, both true.

**TIME:** 20 min.

**DONE WHEN:** You can compute a CI on a *difference* between two strategies, explain in two sentences why statistical and economic significance are separate questions, and spot the wrong version - declaring replication success from a point estimate that is "close to the paper's" without any interval, or declaring failure because your number is smaller (see `RS1` in `python tools/spot_it_wrong.py`).
