---
id: C05
name: Annualization
tier: 2
phase: P2
week: 3
triggered_by: D05
trigger: Your engine prints daily numbers and every sane comparison is annual.
---

# 📐 CONCEPT: Annualization

**WHY NOW:** Your engine's first output is a daily number: 0.04% per day, 1.1% daily volatility. You cannot compare that to a benchmark, a bond, or a friend's returns without putting everything on the same clock - and you are about to compare your strategy to buy-and-hold, which is quoted per year.

**FORMULA:** annualised mean return = mean_daily × 252; annualised volatility = std_daily × √252; CAGR = (final/initial)^(252/n_bars) − 1. Means scale linearly, deviations by the square root.

**CODE:**

```python
import numpy as np, pandas as pd
from kit import metrics as m
d = equity.pct_change().dropna()
ann_ret = d.mean() * m.periods_per_year(d.index)
ann_vol = d.std(ddof=1) * np.sqrt(m.periods_per_year(d.index))
print(f"{ann_ret:+.2%}/yr, vol {ann_vol:.2%}/yr  (infer the frequency, never hardcode 252)")
```

**EXAMPLE:** Your weekly strategy prints a mean weekly return of 0.15%. Annualised: 0.15% × 52 = 7.8%. If you had hardcoded 252, you would report 37.8% and build a whole verdict on a frequency bug. `periods_per_year` infers from the index: daily business bars → 252, weekly → 52, monthly → 12.

**TIME:** 15 min.

**DONE WHEN:** You can code annualisation from a return series and explain in two sentences why volatility scales with the square root while returns scale linearly; you can also spot the wrong version - a Sharpe multiplied by 12 for daily data (the `AN1` snippet in `python tools/spot_it_wrong.py`).
