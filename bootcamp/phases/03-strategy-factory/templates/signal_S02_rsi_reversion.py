"""S02 - short-horizon reversion (the cost graveyard's most popular resident).

Family:    mean reversion, single asset
Thesis:    short-term oversold conditions in liquid ETFs partly reflect forced or
           impatient selling that reverses within days.
Fails how: COSTS. The signal trades often; the gross edge is real but small, and the
           spread plus slippage eats it between 5 and 20 bps round-trip. Log the
           breakeven - it is the week's most instructive number.

Expected shape: excellent gross Sharpe, average net Sharpe near zero, breakeven in
single-digit bps. If yours survives 20 bps, check for look-ahead before celebrating.
Copy to: strategies/S02_rsi_reversion/signal.py
"""

import pandas as pd


def rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0.0, float("nan"))
    return 100.0 - 100.0 / (1.0 + rs)


def generate(prices, params):
    period = int(params.get("period", 2))
    entry = float(params.get("entry", 10.0))     # enter long when RSI drops below this
    exit_ = float(params.get("exit", 60.0))      # leave when RSI recovers above this
    weight = 1.0 / max(len(prices), 1)
    columns = {}
    for symbol, frame in prices.items():
        values = rsi(frame["close"], period)
        position = 0.0
        path = []
        for value in values.tolist():
            if position == 0.0 and value == value and value < entry:
                position = weight                   # raw signal; the engine shifts it
            elif position > 0.0 and value == value and value > exit_:
                position = 0.0
            path.append(position)
        columns[symbol] = pd.Series(path, index=frame.index)
    return pd.DataFrame(columns)
