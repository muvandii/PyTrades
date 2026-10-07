"""S06 - pairs trading on a rolling hedge ratio (spread reversion).

Family:    relative value / statistical arbitrage
Thesis:    two economically related assets share a common factor; deviations of their
           spread are liquidity events that revert over days.
Fails how: the relationship BREAKS. A merger, an index change, a business divergence,
           or a regime shift turns the spread into a trend, and the position becomes a
           bet against a permanent change. Rolling estimation keeps you honest about
           the hedge ratio but cannot save you from a genuine break.

Expected shape: good in-sample Sharpe, decay over time, and a visible widening of the
spread in the last part of the sample. Pair selection on the training window only.
Copy to: strategies/S06_pairs/signal.py
"""

import numpy as np
import pandas as pd


def generate(prices, params):
    window = int(params.get("window", 60))
    entry_z = float(params.get("entry_z", 2.0))
    exit_z = float(params.get("exit_z", 0.5))
    symbols = sorted(prices.keys())
    if len(symbols) < 2:
        raise ValueError("S06 needs two symbols in the universe")

    left = prices[symbols[0]]["close"].astype(float)
    right = prices[symbols[1]]["close"].astype(float)
    log_left = np.log(left)
    log_right = np.log(right)

    covariance = log_left.rolling(window).cov(log_right)
    variance = log_right.rolling(window).var()
    beta = covariance / variance.replace(0.0, float("nan"))
    spread = log_left - beta * log_right
    z = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()

    weights = pd.DataFrame(0.0, index=left.index, columns=symbols)
    position = 0.0
    for i, value in enumerate(pd.Series(z).tolist()):
        if position == 0.0 and value == value and abs(value) > entry_z:
            position = -1.0 if value > 0 else 1.0
        elif position != 0.0 and value == value and abs(value) < exit_z:
            position = 0.0
        if position != 0.0:
            weights.iloc[i, weights.columns.get_loc(symbols[0])] = 0.5 * position
            weights.iloc[i, weights.columns.get_loc(symbols[1])] = -0.5 * position
    return weights
