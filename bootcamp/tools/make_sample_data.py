#!/usr/bin/env python3
"""make_sample_data.py - build the offline laboratory (sample-data/).

These CSVs are SIMULATED, with planted properties, for two jobs:

1. Offline smoke tests: a student with no network can still run the entire pipeline.
2. Exercises with known answers: "did my code find the edge that is definitely there?"
   and "did it find an edge that is definitely not there?" are both gradeable.

They are not market data. `truth.json` records exactly what was planted, so a
student's conclusion can be checked against ground truth - which is impossible with
real markets and is precisely why this lab exists.

Usage:
    python bootcamp/tools/make_sample_data.py            # write sample-data/
    python bootcamp/tools/make_sample_data.py --check    # verify files are current
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Dict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coursekit as ck  # noqa: E402

OUT_DIR = "shared/sample-data"
START = "2010-01-01"
BARS = 2600
SEED = 20260101


def _frame(close: np.ndarray, index: pd.DatetimeIndex, rng: np.random.Generator, spread: float = 0.0015) -> pd.DataFrame:
    close = np.asarray(close, dtype=float)
    open_ = close * (1 + rng.normal(0, spread / 3, len(close)))
    high = np.maximum(close, open_) * (1 + np.abs(rng.normal(0, spread / 2, len(close))))
    low = np.minimum(close, open_) * (1 - np.abs(rng.normal(0, spread / 2, len(close))))
    frame = pd.DataFrame(
        {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": rng.integers(5e5, 5e6, len(close)).astype(float),
        },
        index=index,
    )
    frame.index.name = "date"
    return frame


def lab_trend(index: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    """LAB_TREND: momentum works. Drift runs in ~120-day regimes; daily returns are autocorrelated."""
    n = len(index)
    drift = np.zeros(n)
    regime = 0.0009
    for i in range(n):
        if i % 120 == 0:
            regime = float(rng.choice([0.0009, -0.0007, 0.0004]))
        drift[i] = regime
    noise = rng.normal(0, 0.009, n)
    # plant autocorrelation: today's noise gets a positive carry from yesterday's
    for i in range(1, n):
        noise[i] += 0.18 * noise[i - 1]
    log_price = np.cumsum(drift + noise)
    return _frame(100 * np.exp(log_price), index, rng)


def lab_random(index: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    """LAB_RANDOM: a strong uptrend and nothing else. Buy-and-hold wins; signals add nothing."""
    n = len(index)
    log_price = np.cumsum(rng.normal(0.0006, 0.010, n))
    return _frame(100 * np.exp(log_price), index, rng)


def lab_mean_reverting(index: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    """LAB_MR: strong reversion to a slow trend. RSI/Bollinger works gross, dies on costs."""
    n = len(index)
    slow_trend = np.cumsum(rng.normal(0.0002, 0.0004, n))
    spread = np.zeros(n)
    for i in range(1, n):
        spread[i] = 0.975 * spread[i - 1] + rng.normal(0, 0.015)   # half-life ~28 bars
    log_price = slow_trend + spread
    return _frame(100 * np.exp(log_price), index, rng)


def lab_pair(index: pd.DatetimeIndex, rng: np.random.Generator) -> Dict[str, pd.DataFrame]:
    """LAB_PAIR_A/B: cointegrated until 80% through the sample, then the relationship breaks."""
    n = len(index)
    log_a = np.cumsum(rng.normal(0.0003, 0.010, n))
    spread = np.zeros(n)
    for i in range(1, n):
        spread[i] = 0.96 * spread[i - 1] + rng.normal(0, 0.008)   # half-life ~17 bars
    break_point = int(n * 0.8)
    drift_after = np.zeros(n)
    drift_after[break_point:] = np.cumsum(np.full(n - break_point, 0.0015))  # structural break
    log_b = 1.3 * log_a + spread + drift_after
    return {"LAB_PAIR_A": _frame(100 * np.exp(log_a), index, rng), "LAB_PAIR_B": _frame(100 * np.exp(log_b), index, rng)}


def lab_vol(index: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    """LAB_VOL: volatility clusters WHO switches and returns fall when vol is high - the vol-targeting lab."""
    n = len(index)
    vol = np.zeros(n)
    vol[0] = 0.010
    for i in range(1, n):
        vol[i] = 0.95 * vol[i - 1] + 0.05 * 0.010
        if rng.random() < 0.012:
            vol[i] = min(vol[i] * 2.6, 0.05)
    # plant the vol-return relationship: mean return falls as volatility rises
    mean_ret = 0.00055 - 0.05 * (vol - 0.010)
    ret = rng.normal(0.0, 1.0, n) * vol + mean_ret
    log_price = np.cumsum(ret)
    frame = _frame(100 * np.exp(log_price), index, rng)
    frame["realised_vol"] = np.nan
    return frame


TRUTH = {
    "_warning": "SIMULATED DATA. Properties below are planted. Never cite these as market evidence.",
    "seed": SEED,
    "sample": {"start": START, "bars": BARS, "frequency": "business daily"},
    "series": {
        "LAB_TREND": {
            "planted": "120-day drift regimes of +9/-7/+4 bps per day, plus 0.18 lag-1 autocorrelation in returns",
            "expected": "trend/momentum family (MA cross, Donchian) should show a positive edge out-of-sample; mean reversion should fail",
            "good_for": "Week 3-6 trend strategies, look-ahead demos (the edge is strong enough that a shift bug is obvious)",
        },
        "LAB_RANDOM": {
            "planted": "pure random walk with +6 bps/day drift, no autocorrelation",
            "expected": "buy-and-hold beats every rule; any rule that beats it must be luck - use it to calibrate what luck looks like",
            "good_for": "Week 1 baselines, Week 6 bootstrap, Week 2 debunk practice (a '94% win rate' rule can be built on it trivially)",
        },
        "LAB_MR": {
            "planted": "Ornstein-Uhlenbeck spread, half-life about 28 bars, around a slow random trend",
            "expected": "mean-reversion family: gross Sharpe approx 0.9, breakeven near 20 bps round-trip - a cost-cliff lab, not a money printer",
            "good_for": "Week 5 RSI/Bollinger, cost-death autopsy (the exact headline of several graveyard entries)",
        },
        "LAB_PAIR_A": {
            "planted": "common stochastic trend; partner B = 1.3 x A + OU spread, half-life approx 17 bars",
            "expected": "cointegration tests pass in-sample; the spread trade works for 80% of the sample",
            "good_for": "Week 6 and Week 8 pairs work",
        },
        "LAB_PAIR_B": {
            "planted": "same as A until bar 2080, then a slow structural break (+15 bps/day drift)",
            "expected": "cointegration FAILS on the full sample but PASSES in-sample; the pair trade dies in the last 20%",
            "good_for": "teaching that cointegration is a property of a period, not of a pair (Week 8 lesson, C18)",
        },
        "LAB_VOL": {
            "planted": "volatility clusters with jumps to 2.6x, and mean returns fall as vol rises",
            "expected": "vol targeting (scale exposure by 1/realised vol) improves risk-adjusted returns versus fixed exposure",
            "good_for": "Week 7 TSMOM replication, Week 10 vol targeting and Monte Carlo",
        },
    },
    "hints": {
        "data_validation": "LAB_VOL was written with a deliberately empty 'realised_vol' column - your validator should flag it, and you must delete the column before use",
        "cost_trap": "LAB_MR is the cost trap: gross Sharpe 0.85 becomes 0.43 at 10 bps and zero at 20 bps - the classic graveyard shape",
        "break_point_bar": 2080,
    },
}


def build() -> Dict[str, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    index = pd.bdate_range(START, periods=BARS)
    frames = {
        "LAB_TREND": lab_trend(index, rng),
        "LAB_RANDOM": lab_random(index, rng),
        "LAB_MR": lab_mean_reverting(index, rng),
        "LAB_VOL": lab_vol(index, rng),
    }
    frames.update(lab_pair(index, rng))
    return frames


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    bc = ck.bootcamp_dir()
    out_dir = os.path.join(bc, OUT_DIR)
    os.makedirs(out_dir, exist_ok=True)

    frames = build()
    payloads: Dict[str, str] = {}
    for name, frame in frames.items():
        buffer = frame.to_csv(float_format="%.6f")
        payloads[name + ".csv"] = buffer
    truth_text = json.dumps(TRUTH, indent=2) + "\n"
    payloads["truth.json"] = truth_text

    if args.check:
        problems = []
        for filename, content in payloads.items():
            path = os.path.join(out_dir, filename)
            if not os.path.exists(path) or ck.read_text(path) != content:
                problems.append(filename)
        if problems:
            print("sample-data is STALE for: %s" % ", ".join(problems), file=sys.stderr)
            print("regenerate: python bootcamp/tools/make_sample_data.py", file=sys.stderr)
            return 1
        print("sample-data is up to date (%d files)" % len(payloads))
        return 0

    for filename, content in payloads.items():
        ck.write_text(os.path.join(out_dir, filename), content)
    print("wrote %d files to %s" % (len(payloads), OUT_DIR))
    for name, frame in frames.items():
        print("  %-12s %5d bars  %8.2f -> %8.2f  (%d synthetic columns)" % (name, len(frame), frame['close'].iloc[0], frame['close'].iloc[-1], frame.shape[1] - 5))
    print("  truth.json   planted properties + expected outcomes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
