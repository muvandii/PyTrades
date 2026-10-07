---
id: C02
name: Expectancy & Profit Factor
tier: 1
phase: P1
week: 1
triggered_by: D02
trigger: You cannot say whether a strategy is good; you can only say it made money.
---

# 📐 CONCEPT: Expectancy & Profit Factor

**WHY NOW:** You have an equity curve and a list of trades, and you are about to say "this looks good". "Good" is not a number. You need a per-trade quantity that survives trade-count changes and that you can compare across strategies with completely different holding periods.

**FORMULA:** expectancy = win_rate × avg_win − loss_rate × avg_loss (per trade, net of costs); profit factor = gross profit ÷ gross loss.

**CODE:**

```python
from kit import metrics as m
stats = m.trade_stats(trades)          # needs a 'pnl' column, net of costs
print({k: round(v, 4) for k, v in stats.items()})
# {'win_rate': 0.62, 'expectancy': 14.3, 'profit_factor': 1.41, 'breakeven_win_rate': 0.48, ...}
```

**EXAMPLE:** Your 10-day mean-reversion rule wins 62% of the time with a 1.4 profit factor: positive expectancy, and the breakeven win rate is 48%, so you have margin. Your trend rule wins 31% of the time - and is still profitable, because the average winner is four times the average loser. Two strategies, opposite personalities, comparable in one number each.

**TIME:** 20 min.

**DONE WHEN:** You can code expectancy from a trade list, explain in two sentences what profit factor adds beyond expectancy, and spot the wrong version - a "profitable" claim that reports win rate with no average win/loss - in a claim you find yourself (see `WR1` in `python tools/spot_it_wrong.py`).
