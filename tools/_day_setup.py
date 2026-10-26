# Shared source snippet (not imported at runtime): builders read this file and
# embed SETUP_CODE as the data-setup cell so every daily notebook is standalone.
SETUP_CODE = r'''
# Setup - run first. Loads bundled sample data, or regenerates identical synthetic data.
import sys, io
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
PROCESSED = BASE / "data" / "processed"

def _one(seed, start_price, mu, sigma, n=252):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-02", periods=n, freq="B")
    lr = rng.normal(loc=mu, scale=sigma, size=n)
    close = start_price * np.exp(np.cumsum(lr))
    open_ = np.empty(n); open_[0] = start_price
    open_[1:] = close[:-1] * np.exp(rng.normal(0, 0.002, size=n - 1))
    intraday = np.abs(rng.normal(0, 0.004, size=n))
    f = pd.DataFrame({"Open": np.round(open_, 4),
        "High": np.round(np.maximum(open_, close) * (1 + intraday), 4),
        "Low": np.round(np.minimum(open_, close) * (1 - intraday), 4),
        "Close": np.round(close, 4), "Adj Close": np.round(close, 4),
        "Volume": rng.integers(800_000, 3_000_000, size=n)}, index=dates)
    f.index.name = "Date"; return f

def make_multi():
    parts = {"DEMO": _one(42, 100.0, 0.0004, 0.011), "ORNG": _one(7, 25.0, 0.0008, 0.018),
             "BANK": _one(123, 250.0, 0.0001, 0.008).loc["2020-04-01":]}
    m = pd.concat(parts, axis=1).swaplevel(0, 1, axis=1)
    fields = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    m = m.reindex(columns=pd.MultiIndex.from_product([fields, ["DEMO", "ORNG", "BANK"]]))
    m.index.name = "Date"; return m

def _find(name):
    for base in [Path.cwd(), *Path.cwd().parents]:
        for cand in (base / "data" / "sample" / name, base.parent / "data" / "sample" / name):
            if cand.exists(): return cand
    return None

multi_path = _find("multi_ticker_ohlcv.csv")
if multi_path is not None:
    multi = pd.read_csv(multi_path, header=[0, 1], index_col=0, parse_dates=True)
else:
    multi = make_multi()
    multi_path = Path.cwd() / "multi_ticker_ohlcv_fallback.csv"; multi.to_csv(multi_path)
demo_path = _find("demo_ohlcv.csv")
df = (pd.read_csv(demo_path, parse_dates=["Date"], index_col="Date")
      if demo_path is not None else _one(42, 100.0, 0.0004, 0.011))
close_panel = multi.loc[:, "Close"].copy()
print("multi:", multi.shape, "| close_panel:", close_panel.shape, "| df:", df.shape)
'''
