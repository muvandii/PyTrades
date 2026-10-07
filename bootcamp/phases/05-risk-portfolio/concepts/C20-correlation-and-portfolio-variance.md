---
id: C20
name: Correlation & Portfolio Variance
tier: 4
phase: P5
week: 10
triggered_by: D15
trigger: Two strategies with Sharpe 1.4 and 1.2 combine into something worse than either.
---

# 📐 CONCEPT: Correlation & Portfolio Variance

**WHY NOW:** You have two survivors. Their Sharpes say the combination should be excellent; the combined equity curve says otherwise. Before you pick weights by feel, you need the arithmetic that decides this - and it is three terms long.

**FORMULA:** for two strategies, `σ_p² = w₁²σ₁² + w₂²σ₂² + 2·w₁·w₂·ρ·σ₁·σ₂`. Equal weight: `σ_p² = (σ₁² + σ₂² + 2ρσ₁σ₂)/4`. Sharpe of the combination depends on ρ, not on the individual Sharpes alone.

**CODE:**

```python
import numpy as np
def combined_sharpe(s1, s2, rho, w=0.5):
    # equal-weight combination of two zero-mean strategies, unit-variance each
    var = w**2 + w**2 + 2*w*w*rho
    mu  = w*s1 + w*s2
    return mu / np.sqrt(var)
for rho in (0.9, 0.5, 0.0, -0.3):
    print(f"rho {rho:+.1f}: combined Sharpe {combined_sharpe(1.4, 1.2, rho):.2f}")
```

**EXAMPLE:** Correlation 0.9: the combined Sharpe is 1.44 - barely better than the best component, for twice the capital and twice the operational surface. Correlation 0.0: 1.84. Correlation −0.3: 2.08, which is what the diversification story promised. The practical implication: before combining, measure ρ on the *common overlap* (usually the shortest OOS window you have, which is exactly when your two strategies look least alike - be suspicious). And remember the asymmetry: correlations rise in crises, so the ρ that matters is the one in your worst months, not the full-sample one. Compute both.

**TIME:** 20 min.

**DONE WHEN:** You can code the two-asset portfolio variance and its combined Sharpe, explain in two sentences why correlation dominates diversification for similar-Sharpe strategies, and spot the wrong version - combining strategies using full-sample correlation while the returns only overlap for a third of both samples (see `CV1` in `python tools/spot_it_wrong.py`).
