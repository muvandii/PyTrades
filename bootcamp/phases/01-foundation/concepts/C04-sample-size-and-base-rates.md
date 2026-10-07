---
id: C04
name: Sample Size & Base Rates
tier: 1
phase: P1
week: 2
triggered_by: D04
trigger: Debunk #2 has 11 trades and you want to call it an edge (or a fraud) either way.
---

# 📐 CONCEPT: Sample Size & Base Rates

**WHY NOW:** You have a claim with 11 trades and a win rate of 82%. You cannot tell whether that is skill or noise, and you are about to write a verdict either way. The honest move is to compute what an 11-trade sample can and cannot support - and to compare it against the base rate for the claim's family.

**FORMULA:** the standard error of a win rate is √(p(1−p)/n); a 95% interval is roughly p ± 1.96 × SE. Independent bets matter, not rows: a 3-year daily backtest of a 20-day hold has ~36 independent bets, not 750 bars.

**CODE:**

```python
import math
n, p = 11, 0.82
se = math.sqrt(p * (1 - p) / n)
print(f"win rate {p:.0%} +- {1.96*se:.0%} on n={n}: [{p-1.96*se:.0%}, {p+1.96*se:.0%}]")
# base rate for the family: coin flips beat nothing - a random entry rule with the same
# holding period wins approximately 50% of the time, so 82% on 11 trades is not proof of anything
```

**EXAMPLE:** Debunk #3's rule: 11 trades, 82% win rate. The 95% interval is roughly [59%, 100%] - consistent with a coin flip, so `inconclusive` is the verdict, not `debunked`. Meanwhile a 400-trade rule with a 55% win rate has an interval of about [50%, 60%], which is thin but real evidence. Same procedure, different evidence strength: the arithmetic tells you which one you are looking at.

**TIME:** 20 min.

**DONE WHEN:** You can code a win-rate interval, explain in two sentences why 750 bars is not 750 bets, and spot the wrong version - a conclusion drawn from a handful of trades presented as a finding (see `SS1` in `python tools/spot_it_wrong.py`).
