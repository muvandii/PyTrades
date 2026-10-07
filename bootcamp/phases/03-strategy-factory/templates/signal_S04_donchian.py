"""S04 - Donchian breakout (the turtle's ancestor, minus the turtle discipline).

Family:    trend following, breakout
Thesis:    new N-day highs mark the arrival of persistent flow (index rebalancing,
           trend-following funds, retail momentum) that continues for days to weeks.
Fails how: false breakouts in chop; many small losses with rare large wins, so the
           trade distribution is extremely skewed (this is the family where win rate
           below 40% is normal, and where win rate tells you least).

Expected shape: 20-40 trades per decade per symbol, sub-40% win rate, profit factor
around 1, and a large sensitivity to the exit rule. Cost-tolerant.
Copy to: strategies/S04_donchian/signal.py
"""

import pandas as pd


def generate(prices, params):
    entry = int(params.get("entry", 20))
    exit_ = int(params.get("exit", 10))
    weight = 1.0 / max(len(prices), 1)   # equal weight per symbol
    columns = {}
    for symbol, frame in prices.items():
        # shift by one bar: today's close is compared with the PRIOR window's extremes
        high = frame["high"].shift(1).rolling(entry, min_periods=entry).max()
        low = frame["low"].shift(1).rolling(exit_, min_periods=exit_).min()
        position = 0.0
        path = []
        for i, close in enumerate(frame["close"].tolist()):
            entry_level = high.iloc[i]
            exit_level = low.iloc[i]
            if entry_level == entry_level and close >= entry_level:
                position = weight
            elif exit_level == exit_level and close <= exit_level:
                position = 0.0
            path.append(position)
        columns[symbol] = pd.Series(path, index=frame.index)
    return pd.DataFrame(columns)
