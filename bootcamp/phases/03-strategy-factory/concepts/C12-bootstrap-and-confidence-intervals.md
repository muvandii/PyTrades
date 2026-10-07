---
id: C12
name: Bootstrap & Confidence Intervals
tier: 3
phase: P3
week: 5
triggered_by: D10
trigger: Two survivors have OOS Sharpe 0.68 and 0.55 and you need to say which is better.
---

# 📐 CONCEPT: Bootstrap & Confidence Intervals

**WHY NOW:** You have two strategies 0.13 apart in Sharpe and the whole verdict hinges on which one to keep. The honest answer requires knowing how much a Sharpe estimate of this sample size *wobbles* - and the only way to get that without assuming normality is to resample the data you actually have.

**FORMULA:** block bootstrap: draw contiguous blocks of length L (≈ holding period in bars) with replacement, concatenate to the original sample length, recompute the statistic; repeat B = 2,000 times; report the 2.5th and 97.5th percentiles as a 95% interval. Blocks, not single bars, because returns are autocorrelated.

**CODE:**

```python
import numpy as np
r = oos_returns.to_numpy(); n = len(r); L = int(holding_bars)   # block length >= holding period
rng = np.random.default_rng(7)
draws = []
for _ in range(2000):
    idx = np.concatenate([np.arange(s, s + L) % n for s in rng.integers(0, n, n // L + 1)])[:n]
    s = r[idx]; draws.append(0 if s.std() == 0 else np.sqrt(252) * s.mean() / s.std(ddof=1))
print("95% CI:", np.round(np.percentile(draws, [2.5, 97.5]), 2))
```

**EXAMPLE:** Your best survivor: OOS Sharpe 0.68, 95% CI [0.21, 1.14] - excludes zero, so the edge is at least *present* in this sample. Second candidate: 0.55, CI [−0.18, 1.19] - includes zero, and overlaps the first completely. The point estimate ranking (0.68 > 0.55) is not a finding; the two strategies are statistically indistinguishable on 3 years of out-of-sample data. This is the answer that goes in the verdict, even though it is less fun than "S01 wins".

**TIME:** 20 min.

**DONE WHEN:** You can code a block bootstrap for Sharpe, explain in two sentences why IID resampling of daily returns understates the uncertainty, and spot the wrong version - a bootstrap that resamples trades and reports a Sharpe interval, or one that re-centres the resampled series to zero mean (see `BS1` in `python tools/spot_it_wrong.py`).
