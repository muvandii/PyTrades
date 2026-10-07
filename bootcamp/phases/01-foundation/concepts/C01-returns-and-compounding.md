---
id: C01
name: Returns & Compounding
tier: 1
phase: P1
week: 1
triggered_by: D02
trigger: Your first equity curve looks like a straight line going up - until you compute what a 50% loss does to it.
---

# 📐 CONCEPT: Returns & Compounding

**WHY NOW:** You have just drawn your first equity curve. It goes up, so you feel good. Then you compute the arithmetic of a -50% year followed by a +50% year and discover you are down 25%. The chart was never a line; it was a product.

**FORMULA:** total return = Π(1 + r_t) − 1, and a −x% loss needs +x/(1−x) to recover (that is +100% for a −50% loss).

**CODE:**

```python
import pandas as pd
returns = spy["close"].pct_change().dropna()
total = (1 + returns).prod() - 1          # compounding: the truth
naive = returns.sum()                      # adding returns: a story
recovery_needed = 1 / (1 + returns.min()) - 1   # what the worst day demanded back
print(f"{total:+.2%} compounded vs {naive:+.2%} added; worst day needed {recovery_needed:+.0%} to recover")
```

**EXAMPLE:** On 20 years of SPY, `returns.sum()` and `(1+returns).prod()-1` differ by several percentage points - and that gap grows with volatility. Every metric later in this course (Sharpe, CAGR, drawdown, Kelly) is built on the compounded curve, so a strategy whose numbers are computed by summing returns is not a strategy, it is a spreadsheet.

**TIME:** 15 min.

**DONE WHEN:** You can code `(1+r).prod()-1` from memory, explain in two sentences why summing returns overstates a volatile strategy, and spot the wrong version - a backtest whose total return is `returns.sum()` - in someone else's notebook (see the `CP1` snippet in `python tools/spot_it_wrong.py`).
