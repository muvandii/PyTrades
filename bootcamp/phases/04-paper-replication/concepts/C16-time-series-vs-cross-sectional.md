---
id: C16
name: Time-Series vs Cross-Sectional
tier: 3
phase: P4
week: 7
triggered_by: D12
trigger: The TSMOM paper's Sharpe comes from a mechanism none of your single-instrument backtests could express.
---

# 📐 CONCEPT: Time-Series vs Cross-Sectional

**WHY NOW:** Your S05 momentum strategy ranked assets against each other and held the winners. TSMOM asks a different question per asset - "is *this* asset trending?" - and holds however many say yes. The two look similar on a chart of returns and are completely different bets, with different diversification.

**FORMULA:** time-series (absolute) momentum: position_i = sign(r_i, past 12m). Cross-sectional (relative) momentum: position_i = rank(r_i, past 12m) − mean, long the top. TSMOM's gross exposure varies through time (market timing); cross-sectional momentum's is roughly constant (relative ranking).

**CODE:**

```python
import pandas as pd
past = closes / closes.shift(252) - 1.0                      # 12-month returns, one column per asset
ts      = past.apply(lambda col: col.apply(lambda r: 0.0 if r != r else (1.0 if r > 0 else -1.0)))
xs      = past.sub(past.mean(axis=1), axis=0).apply(lambda col: col / past.std(axis=1))   # relative
print("TSMOM gross exposure over time:", ts.abs().sum(axis=1).mean().round(2))            # varies
print("cross-sectional gross exposure: ", xs.abs().sum(axis=1).mean().round(2))           # ~constant
```

**EXAMPLE:** On 2008 data, the TSMOM book would be *short* three of four asset classes because each was individually trending down - a bet the cross-sectional version cannot make, because it is always long the relative winners. That difference is why TSMOM diversifies across markets while cross-sectional momentum diversifies across time: TSMOM's edge comes from many weakly correlated markets all having trends, so running it on three correlated equity ETFs is running it without its engine.

**TIME:** 20 min.

**DONE WHEN:** You can code both position schemes from the same momentum forecast, explain in two sentences why they diversify differently, and spot the wrong version - a "TSMOM" backtest where the plus and minus positions always sum to a constant gross exposure (that is cross-sectional wearing a TSMOM nametag; see `TS1` in `python tools/spot_it_wrong.py`).
