---
id: C03
name: Win Rate vs Edge
tier: 1
phase: P1
week: 2
triggered_by: D03
trigger: The "90% win rate" strategy you are debunking has a 90% win rate - and still loses.
---

# 📐 CONCEPT: Win Rate vs Edge

**WHY NOW:** You just reproduced a viral claim's 90% win rate on real data. Your job now is to say why it still loses money, in one sentence a non-quant understands. The sentence is: a win rate is half of an expectancy, and the other half is how big the loser is.

**FORMULA:** edge = win_rate × avg_win − loss_rate × avg_loss; breakeven_win_rate = avg_loss / (avg_win + avg_loss).

**CODE:**

```python
from kit import metrics as m
win_rate = m.win_rate(trades)                  # the marketing number
breakeven = m.breakeven_win_rate(trades)       # the number that decides
print(f"wins {win_rate:.0%} of trades; needs {breakeven:.0%} to break even -> {'EDGE' if win_rate > breakeven else 'NO EDGE'}")
```

**EXAMPLE:** 90 trades of +1 and 10 trades of −15: win rate 90%, expectancy −0.6 per trade, profit factor 0.6, breakeven win rate 93.75%. The strategy is a machine that pays out small and takes back large - the shape of most premium-selling blowups and most viral "90% win rate" posts.

**TIME:** 15 min.

**DONE WHEN:** You can code win rate and breakeven win rate side by side, explain in two sentences why a high win rate with negative skew is the most dangerous shape, and spot the wrong version - a strategy marketed on win rate alone - in the next claim you read (see `WR1` in `python tools/spot_it_wrong.py`).
