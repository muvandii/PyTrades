---
id: C25
name: Regime Detection
tier: 5
phase: P6
week: 12
triggered_by: D17
trigger: Your entire live divergence is one volatile month, not a bug.
---

# 📐 CONCEPT: Regime Detection

**WHY NOW:** Before you spend the weekend hunting a phantom bug, check the possibility that your live window simply was not the backtest's average month. Markets have states - high and low volatility, trending and chopping - and a strategy's behaviour in each state is a fact about the strategy that you can measure.

**FORMULA:** the simplest useful regime variable is realised volatility: `σ_t = std(r_{t−20:t}) × √252`, split at its historical median (or its 75th percentile for a "crisis" state). Compare performance in each state; scale the expected divergence by the share of the live window in each state. (Hidden Markov models exist and are overkill here; you need *an observable state variable*, not the true ones.)

**CODE:**

```python
import numpy as np, pandas as pd
r = portfolio_returns
vol20 = r.rolling(20).std() * np.sqrt(252)
state = np.where(vol20 > vol20.expanding(60).median(), "high-vol", "low-vol")     # causal, no look-ahead
perf = pd.DataFrame({"ret": r, "state": pd.Series(state, index=r.index)})
print(perf.groupby("state")["ret"].agg(["mean", "std", "count"]).round(5))
share = (perf["state"] == "high-vol").mean(); print("high-vol share:", round(share, 2))
```

**EXAMPLE:** Your live window: 40% of days classified high-vol against a 50% historical share - i.e. a *quiet* month by your own measure. Re-running the shadow backtest restricted to historical quiet months predicts +0.2% for the window; live returned −0.1%. The 30 bps of divergence is regime, not implementation, and now three different explanations have been checked and dismissed or accepted on evidence. Only then do you start looking for bugs - and you look at the log, not at the strategy.

**TIME:** 20 min.

**DONE WHEN:** You can compute an observable, causal regime classification and compare strategy behaviour across states, explain in two sentences why a regime-conditional expectation is the right benchmark for a short live window, and spot the wrong version - classifying the *outcome* (calling a losing month "high-vol" after the fact) rather than classifying the state using information available at the time (see `RG1` in `python tools/spot_it_wrong.py`).
