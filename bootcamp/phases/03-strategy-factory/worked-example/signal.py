"""S03 - Bollinger / z-score reversion (the worked example).

Family:    mean reversion around a moving average
Thesis:    price deviations from a short-window mean partly revert, because most
           flow in index ETFs is liquidity-driven rather than information-driven.
Fails how: two ways. Costs (it trades often), and regime (a genuine trend after a
           shock keeps the "oversold" asset oversold for weeks).

Expected shape: gross Sharpe 0.8-1.5, net Sharpe falling to ~0 by 10-20 bps.
The worked example in ../worked-example/ shows the full write-up.
Copy to: strategies/S03_bollinger/signal.py
"""

import pandas as pd


def generate(prices, params):
    window = int(params.get("window", 20))
    entry_z = float(params.get("entry_z", -2.0))
    exit_z = float(params.get("exit_z", 0.0))
    allow_short = bool(params.get("allow_short", False))

    weight = 1.0 / max(len(prices), 1)
    columns = {}
    for symbol, frame in prices.items():
        close = frame["close"]
        mean = close.rolling(window, min_periods=window).mean()
        std = close.rolling(window, min_periods=window).std(ddof=1)
        z = (close - mean) / std.replace(0.0, float("nan"))
        position = 0.0
        path = []
        for value in z.tolist():
            if position == 0.0 and value == value:
                if value <= entry_z:                     # entry_z is negative, e.g. -2
                    position = weight
                elif allow_short and value >= abs(entry_z):
                    position = -weight
            if position > 0.0 and value == value and value >= exit_z:
                position = 0.0
            elif position < 0.0 and value == value and value <= -exit_z:
                position = 0.0
            path.append(position)
        columns[symbol] = pd.Series(path, index=frame.index)
    return pd.DataFrame(columns)
