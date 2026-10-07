---
id: C18
name: Cointegration & Spreads
tier: 3
phase: P4
week: 8
triggered_by: D13
trigger: Two assets drift apart forever and your "mean reversion" trade becomes a trend trade - against you.
---

# 📐 CONCEPT: Cointegration & Spreads

**WHY NOW:** S06's pairs trade worked in-sample on the full sample and stopped exactly where you needed it. You need a *test* for whether two prices are linked by something that survives, because "they look related" is how a pairs strategy becomes a two-legged short squeeze.

**FORMULA:** spread_t = log(P_A) − β·log(P_B), β from OLS on the formation window; half-life = −ln(2)/λ from the regression Δspread_t = λ·spread_{t−1} + ε_t; test with ADF (or `statsmodels.tsa.stattools.coint`) - reject the unit root only if the p-value is small *and* the half-life is short enough to trade.

**CODE:**

```python
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
beta = sm.OLS(np.log(a), sm.add_constant(np.log(b))).fit().params[1]
spread = np.log(a) - beta * np.log(b)
p = coint(np.log(a), np.log(b))[1]
lam = sm.OLS(spread.diff().dropna(), sm.add_constant(spread.shift(1).dropna())).fit().params[1]
print(f"beta {beta:.3f}  coint p {p:.3f}  half-life {-np.log(2)/lam:.0f} bars  ADF p {adfuller(spread)[1]:.3f}")
```

**EXAMPLE:** KO/PEP on the formation window: β 1.09, coint p 0.04, half-life 24 bars - a relationship you can trade with a two-week horizon. A different candidate pair: coint p 0.71, half-life 180 bars - the spread is a random walk, and a 2σ deviation is just a random number; entering it is trend-following with worse framing. Same code, opposite decisions. The half-life also sets the maximum holding period: if 24 bars is the half-life, holding 120 bars waiting for convergence is a decision to be flat-out wrong for a month.

**TIME:** 20 min.

**DONE WHEN:** You can estimate β, run a cointegration test, compute a half-life, and explain in two sentences why a long half-life (or a high p-value) means the trade is not pairs trading at all; you can also spot the wrong version - a pairs trade selected by highest price correlation with no test of the residual, or a z-score computed on a spread whose β was fitted on the same window it is traded in (see `PJ1` in `python tools/spot_it_wrong.py`).
