---
id: C13
name: Parameter Sensitivity & Plateaus
tier: 3
phase: P3
week: 5
triggered_by: D11
trigger: One sweep shows a smooth hill and the next shows a single spike, both with the same best Sharpe.
---

# 📐 CONCEPT: Parameter Sensitivity & Plateaus

**WHY NOW:** You swept your MA windows and found the best pair. So did you find a property of the market, or the coordinates of your own search? The shape of the surface around the peak answers this - and it answers it before any out-of-sample test is even run.

**FORMULA:** over a parameter grid, `plateau` = contiguous region within ~10% of peak Sharpe; `spike` = peak neighbours drop below half. Report plateau width in parameter units, not as a picture.

**CODE:**

```python
import numpy as np, pandas as pd
grid = pd.read_csv("reports/sensitivity/S01_ma_cross.csv")   # rows: fast, cols: slow, values: sharpe
peak = grid.values.max(); near = grid.values >= 0.9 * peak
print(f"peak {peak:.2f}, cells within 10%: {near.sum()}/{grid.size}, width ~{near.sum() ** 0.5:.1f} std")
print("surface:", "plateau" if near.mean() > 0.2 else "ridge" if near.any() else "spike")
```

**EXAMPLE:** S01: peak Sharpe 0.72 at (fast 45, slow 190); cells within 10% of the peak span fast 30-70 and slow 150-240 - roughly 6% of the whole grid, a broad plateau. The neighbouring cells are not a cliff. If instead the peak were 1.4 and its four neighbours were 0.3, you would have found *your search's* coordinates: nothing that fragile is a market property, and the OOS test would mostly measure your luck.

**TIME:** 20 min.

**DONE WHEN:** You can compute a grid, classify each surface as plateau / ridge / spike with a rule rather than a feeling, and explain in two sentences why plateau width is evidence about the *market* while peak height is evidence about your *search*; you can also spot the wrong version - reading the best cell off a 3×3 grid and calling it robust (see `PS1` in `python tools/spot_it_wrong.py`).
