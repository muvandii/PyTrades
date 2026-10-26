"""Generate the deterministic, synthetic OHLCV sample used on Day 01.

This is NOT real market data. It exists so every graded exercise runs
offline and reproducibly, even when Yahoo Finance is unreachable or the
yfinance return format changes (as it has since the 2022 video).

Run from the repository root:
    python tools/generate_sample_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd


def make_demo_ohlcv(n: int = 252, seed: int = 42) -> pd.DataFrame:
    """Return one synthetic trading year of daily OHLCV bars."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-02", periods=n, freq="B")

    # Geometric random walk: close[t] = close[t-1] * exp(log_return[t])
    log_returns = rng.normal(loc=0.0004, scale=0.011, size=n)
    close = 100.0 * np.exp(np.cumsum(log_returns))

    open_ = np.empty(n)
    open_[0] = 100.0
    open_[1:] = close[:-1] * np.exp(rng.normal(0, 0.002, size=n - 1))

    intraday = np.abs(rng.normal(0, 0.004, size=n))
    high = np.maximum(open_, close) * (1 + intraday)
    low = np.minimum(open_, close) * (1 - intraday)
    volume = rng.integers(800_000, 3_000_000, size=n)

    df = pd.DataFrame(
        {
            "Open": np.round(open_, 4),
            "High": np.round(high, 4),
            "Low": np.round(low, 4),
            "Close": np.round(close, 4),
            "Adj Close": np.round(close, 4),
            "Volume": volume,
        },
        index=dates,
    )
    df.index.name = "Date"
    return df


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "data" / "sample" / "demo_ohlcv.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    frame = make_demo_ohlcv()
    frame.to_csv(out)
    print(f"Wrote {out} rows={len(frame)} {frame.index.min().date()}..{frame.index.max().date()}")
