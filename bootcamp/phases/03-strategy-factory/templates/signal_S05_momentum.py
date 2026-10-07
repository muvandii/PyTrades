"""S05 - cross-sectional momentum (12-1), monthly rebalance.

Family:    cross-sectional trend
Thesis:    assets that outperformed over the past year tend to keep outperforming for
           the next month (Moskowitz/Ooi/Pedersen 2012; Jegadeesh/Titman 1993), because
           information diffuses slowly and flows chase performance.
Fails how: momentum crashes - the strategy owns whatever just ran hardest and takes
           the full hit of the reversal; also crowded at the end of bull markets.

Expected shape: positive net Sharpe in most samples, occasional -20% months, and a
strong dependence on the universe (needs a wide set, not two correlated ETFs).
Copy to: strategies/S05_momentum/signal.py
"""

import pandas as pd


def generate(prices, params):
    lookback = int(params.get("lookback", 252))
    skip = int(params.get("skip", 21))
    top_n = int(params.get("top_n", 3))
    closes = pd.DataFrame({symbol: frame["close"] for symbol, frame in prices.items()})
    momentum = closes.shift(skip) / closes.shift(skip + lookback) - 1.0
    weights = pd.DataFrame(0.0, index=closes.index, columns=closes.columns)
    for i, (timestamp, row) in enumerate(momentum.iterrows()):
        valid = row.dropna()
        if len(valid) < top_n:
            continue
        winners = valid.nlargest(top_n).index
        for symbol in winners:
            weights.iloc[i, weights.columns.get_loc(symbol)] = 1.0 / top_n
    return weights
