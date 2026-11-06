"""Generate the deterministic, synthetic OHLCV samples used across PyTrades.

This is NOT real market data. It exists so every graded exercise runs
offline and reproducibly, even when Yahoo Finance is unreachable or the
yfinance return format changes (as it has since the 2022 video).

Outputs:
  - data/sample/demo_ohlcv.csv      (252 business days, Week 1 single-ticker)
  - data/sample/long_spy_like.csv   (2,520 business days ~10y, Week 2 backtests)

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


def make_long_spy_like(
    seed: int = 808, start_price: float = 180.0, n: int = 2520
) -> pd.DataFrame:
    """Return ~10 synthetic trading years (2,520 business days) of daily OHLCV bars.

    Designed for Week 2 SMA50/100/200 crossover backtests: deterministic seed,
    plausible multi-regime equity-index drift and volatility (steady bull,
    mid-cycle chop, sharp crisis & recovery, bear regime, renewed expansion).
    SYNTHETIC educational data - not real SPY prices.
    """
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2015-01-02", periods=n, freq="B")
    regimes = [
        (680, 0.00050, 0.0080),
        (250, -0.00025, 0.0115),
        (110, -0.00220, 0.0220),
        (560, 0.00095, 0.0105),
        (320, -0.00085, 0.0140),
        (600, 0.00065, 0.0090),
    ]
    total_regime_len = sum(length for length, _, _ in regimes)
    if total_regime_len != n:
        lr = rng.normal(loc=0.00035, scale=0.011, size=n)
    else:
        lr = np.concatenate([rng.normal(mu, sig, length) for length, mu, sig in regimes])
    lr[0] = 0.0
    close = start_price * np.exp(np.cumsum(lr))

    open_ = np.empty(n)
    open_[0] = start_price
    open_[1:] = close[:-1] * np.exp(rng.normal(0, 0.0018, size=n - 1))

    intraday = np.abs(rng.normal(0, 0.0045, size=n))
    high = np.maximum(open_, close) * (1 + intraday)
    low = np.minimum(open_, close) * (1 - intraday)
    volume = rng.integers(2_000_000, 9_000_000, size=n)

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
    sample_dir = Path(__file__).resolve().parents[1] / "data" / "sample"
    sample_dir.mkdir(parents=True, exist_ok=True)

    demo_out = sample_dir / "demo_ohlcv.csv"
    frame = make_demo_ohlcv()
    frame.to_csv(demo_out)
    print(f"Wrote {demo_out} rows={len(frame)} {frame.index.min().date()}..{frame.index.max().date()}")

    long_out = sample_dir / "long_spy_like.csv"
    long_frame = make_long_spy_like()
    long_frame.to_csv(long_out)
    print(
        f"Wrote {long_out} rows={len(long_frame)} "
        f"{long_frame.index.min().date()}..{long_frame.index.max().date()}"
    )
