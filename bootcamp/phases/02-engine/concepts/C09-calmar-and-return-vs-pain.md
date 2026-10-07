---
id: C09
name: Calmar & Return-vs-Pain
tier: 2
phase: P2
week: 4
triggered_by: D07
trigger: Two strategies with similar returns, radically different drawdowns: Sharpe says tie.
---

# 📐 CONCEPT: Calmar & Return-vs-Pain

**WHY NOW:** Two of your strategies have Sharpe 0.9 and 0.88. One never lost more than 12%; the other lost 44% once and took three years to recover. Sharpe is blind to that difference, and you have to choose. You need a ratio whose denominator is pain, not wobble.

**FORMULA:** Calmar = CAGR / |max drawdown|; Ulcer index = √mean(drawdown²) (how much pain, not just how deep); recovery factor = total return / |max drawdown|.

**CODE:**

```python
from kit import metrics as m
r = m.to_returns(equity)
print(f"calmar {m.calmar(r, equity):.2f}   ulcer {m.ulcer_index(equity):.1%}   recovery factor {m.recovery_factor(r, equity):.2f}")
```

**EXAMPLE:** Strategy A: CAGR 12%, maxDD 44% → Calmar 0.27. Strategy B: CAGR 9%, maxDD 11% → Calmar 0.82. Same Sharpe ballpark, but B is the one you can size up, hold through, and explain to someone else without a chart. Calmar is not "better" than Sharpe - it is the ratio that answers a question Sharpe cannot hear.

**TIME:** 15 min.

**DONE WHEN:** You can code Calmar and Ulcer, explain in two sentences when you would prefer Calmar to Sharpe (long drawdowns, capital you must not lose), and spot the wrong version - a Calmar computed with the average drawdown instead of the maximum, or a "return/drawdown" using the sum of returns (see `CP1` and `DD1` in `python tools/spot_it_wrong.py`).
