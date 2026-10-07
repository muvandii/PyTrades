---
id: C23
name: Slippage Modeling & Latency
tier: 5
phase: P6
week: 11
triggered_by: D16
trigger: Live fills are systematically worse than the close your backtest assumed.
---

# 📐 CONCEPT: Slippage Modeling & Latency

**WHY NOW:** Your backtest fills at the next open, your bot submits an order at 07:12 and gets a fill three seconds later at a different price. Over a month that difference is a real, measurable drag - and until you model it, every live comparison will show a mysterious "unexplained" bucket.

**FORMULA:** total execution cost = spread cost (half-spread per side) + market-impact (grows with size/ADV, usually ~ sqrt) + timing drift (price move between decision and fill) + fees. In bps of notional: `cost_bps ≈ 0.5·spread_bps + k·√(size/ADV) + drift_bps`.

**CODE:**

```python
# measure it from your own logs instead of assuming it
fills = pd.DataFrame([{"ts": f["ts"], "px": f["price"], "ref": ref_price[f["symbol"]]} for f in all_fills])
fills["slip_bps"] = 1e4 * (fills["px"] / fills["ref"] - 1.0)          # signed: positive = paid more
print(fills.groupby("symbol")["slip_bps"].agg(["mean", "std", "count"]).round(1))
print("median realised:", float(fills["slip_bps"].median()), "bps  (use this in the backtest, not your assumption)")
```

**EXAMPLE:** Your paper adapter assumed 2 bps slippage; your logs show a median 6.4 bps on the momentum leg and 1.8 bps on the ETF leg. Re-running the backtest with the *measured* numbers instead of the assumed ones moves the predicted month from +0.9% to +0.55% - and suddenly the live/backtest gap is mostly explained before you look for bugs. That is the whole discipline: measure your ledger of frictions, feed it back into the backtest, and compare again.

**TIME:** 20 min.

**DONE WHEN:** You can compute realised slippage from your own fill logs, explain in two sentences why slippage is asymmetric (you buy after good news, sell after bad) and why that makes it a *cost* rather than noise, and spot the wrong version - a backtest with zero slippage, or a slippage assumption that is a round 10 bps for instruments whose spreads differ 5× (see `SL1` in `python tools/spot_it_wrong.py`).
