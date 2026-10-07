"""S01 - moving-average cross (the trend family's hello world).

Family:    trend following
Thesis:    slow-moving capital keeps buying after prices rise; the cross is a
           crude proxy for "the average participant is now wrong-footed".
Fails how: whipsaw in chop (many small losses), and the 50/200 cross is so widely
           watched that any edge is small and slow. Cost death is rare here
           (turnover ~1x/year), which makes it a good first family to test.

Expected shape: a handful of trades per decade, equity curve resembling buy-and-hold
slightly smoothed, Sharpe modestly better or worse than the benchmark.
Copy to: strategies/S01_ma_cross/signal.py
"""

import pandas as pd


def generate(prices, params):
    fast = int(params.get("fast", 50))
    slow = int(params.get("slow", 200))
    weight = 1.0 / max(len(prices), 1)   # equal weight; never stack full size on every symbol
    columns = {}
    for symbol, frame in prices.items():
        close = frame["close"]
        fast_ma = close.rolling(fast, min_periods=fast).mean()
        slow_ma = close.rolling(slow, min_periods=slow).mean()
        columns[symbol] = (fast_ma > slow_ma).astype(float) * weight
    return pd.DataFrame(columns)
