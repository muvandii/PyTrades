---
id: C15
name: Overfitting & Walk-Forward Honesty
tier: 3
phase: P3
week: 6
triggered_by: D11
trigger: In-sample Sharpe 2.1, out-of-sample Sharpe -0.2, and you are sure it is "just that one window".
---

# 📐 CONCEPT: Overfitting & Walk-Forward Honesty

**WHY NOW:** One of your strategies printed a beautiful 2.1 Sharpe in-sample and something like −0.2 out. That gap is not bad luck - it is the normal signature of selecting parameters on the same data you report results from. Understanding the mechanism is what stops you from "fixing" it by trying more parameters.

**FORMULA:** the expected inflation of the best-of-N search is roughly `E[max Sharpe] ≈ σ_sharpe × √(2 ln N)`; with σ_sharpe ≈ 1/√years, trying 50 specifications on 3 years of data inflates the reported Sharpe by ~0.8 even when no edge exists.

**CODE:**

```python
import numpy as np
years = 3.0; n_specs = 50
inflation = np.sqrt(1 / years) * np.sqrt(2 * np.log(n_specs))
print(f"expected maximum Sharpe from pure luck across {n_specs} specs and {years} years: {inflation:.2f}")
# and the honest estimator: pooled OOS sharpe, every split, incl. the bad ones
```

**EXAMPLE:** You tested 40 MA variants; the best IS Sharpe was 1.4. The deflation from the formula alone is ~0.7, so your honest expectation before OOS was ~0.7 - and your pooled OOS printed 0.4. Verdict: the effect exists but it is roughly *half the size you first saw*, and the kill criterion should be written against 0.4, not 1.4. That is what "the walk-forward is the result" means: the pooled OOS number, all splits included, is the number you report.

**TIME:** 20 min.

**DONE WHEN:** You can estimate the deflation from your own specification count, explain in two sentences why trying more parameters on the same data does not fix overfitting, and spot the wrong version - a verdict that reports the best split's OOS number, or an IS Sharpe with the word "conservative" attached (see `OV1` in `python tools/spot_it_wrong.py`).
