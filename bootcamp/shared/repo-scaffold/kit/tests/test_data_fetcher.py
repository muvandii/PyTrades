"""Tests for kit/data_fetcher.py - the data layer's contract with the rest of the repo.

These are deliberately network-free: the fetchers themselves are exercised by
`python -m kit.data_fetcher smoke`, and everything below tests logic that must hold
whether or not the network is up.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kit import data_fetcher as df  # noqa: E402


# --------------------------------------------------------------------------- #
# synthetic(): the offline workhorse
# --------------------------------------------------------------------------- #
def test_synthetic_is_deterministic_for_a_seed():
    a = df.synthetic("SYN", "2015-01-01", "2016-12-31", seed=42)
    b = df.synthetic("SYN", "2015-01-01", "2016-12-31", seed=42)
    assert a.equals(b)
    c = df.synthetic("SYN", "2015-01-01", "2016-12-31", seed=43)
    assert not a["close"].equals(c["close"])


def test_synthetic_has_the_ohlcv_contract():
    frame = df.synthetic("SYN", "2015-01-01", "2017-12-31")
    assert set(["open", "high", "low", "close", "volume"]).issubset(frame.columns)
    assert isinstance(frame.index, pd.DatetimeIndex)
    assert frame.index.is_monotonic_increasing
    assert (frame["high"] >= frame["low"]).all()
    assert (frame["high"] >= frame["close"]).all()
    assert (frame["low"] <= frame["close"]).all()


def test_synthetic_volatility_stays_inside_the_documented_clip():
    # the generator clips *daily* vol to [0.003, 0.055] (annualised ~4.8%..87%)
    frame = df.synthetic("SYN", "2015-01-01", "2024-12-31")
    r = frame["close"].pct_change().dropna()
    assert r.abs().max() < 0.20, "a single daily move above 20%% means the clip is not applied"
    rolling_vol = (r.rolling(20).std() * np.sqrt(252)).dropna()
    assert rolling_vol.min() > 0.01
    assert rolling_vol.max() < 1.5


def test_synthetic_is_flagged_and_refused_by_assert_not_synthetic(tmp_path):
    frame = df.synthetic("SYN", "2015-01-01", "2016-12-31")
    path = df._persist(frame, "SYN", "synthetic", str(tmp_path))
    meta = df.read_meta("SYN", str(tmp_path))
    assert meta.get("synthetic") is True
    loaded = df.load("SYN", str(tmp_path))
    with pytest.raises(ValueError):
        df.assert_not_synthetic(loaded, "SYN")


# --------------------------------------------------------------------------- #
# validate(): what the pipeline trusts
# --------------------------------------------------------------------------- #
def test_validate_accepts_a_clean_frame():
    frame = df.synthetic("SYN", "2015-01-01", "2016-12-31")
    report = df.validate(frame, "SYN")
    assert report.ok
    assert not report.issues


def test_validate_flags_nan_in_close():
    frame = df.synthetic("SYN", "2015-01-01", "2016-12-31").copy()
    frame.iloc[10, frame.columns.get_loc("close")] = np.nan
    report = df.validate(frame, "SYN")
    assert not report.ok


def test_validate_flags_non_positive_prices():
    frame = df.synthetic("SYN", "2015-01-01", "2016-12-31").copy()
    frame.iloc[10, frame.columns.get_loc("close")] = -1.0
    report = df.validate(frame, "SYN")
    assert not report.ok


def test_validate_flags_duplicate_dates():
    frame = df.synthetic("SYN", "2015-01-01", "2016-12-31")
    doubled = pd.concat([frame, frame.iloc[[5]]]).sort_index()
    report = df.validate(doubled, "SYN")
    assert not report.ok


def test_validate_reports_the_window_it_actually_saw():
    frame = df.synthetic("SYN", "2015-01-01", "2015-06-30")
    report = df.validate(frame, "SYN")
    assert str(report.first)[:4] == "2015"
    assert str(report.last)[:4] == "2015"
    assert "2015-01-01" in str(report.first)


# --------------------------------------------------------------------------- #
# fetch(): cache, fallback, and the synthetic opt-in
# --------------------------------------------------------------------------- #
def test_fetch_prefers_fresh_cache_without_network(tmp_path, monkeypatch):
    frame = df.synthetic("CACHEME", "2015-01-01", "2016-12-31")
    df._persist(frame, "CACHEME", "synthetic", str(tmp_path))

    def explode(*args, **kwargs):  # pragma: no cover - must never be called
        raise AssertionError("network should not be touched when the cache is fresh")

    monkeypatch.setattr(df, "PROVIDERS", {"stooq": explode, "yahoo": explode})
    out = df.fetch("CACHEME", data_dir=str(tmp_path))
    assert len(out) > 100


def test_fetch_without_network_raises_unless_synthetic_is_allowed(tmp_path, monkeypatch):
    def boom(*args, **kwargs):
        raise OSError("no network in tests")

    monkeypatch.setattr(df, "PROVIDERS", {"stooq": boom, "yahoo": boom})
    with pytest.raises(RuntimeError):
        df.fetch("NONET", data_dir=str(tmp_path))
    out = df.fetch("NONET", data_dir=str(tmp_path), allow_synthetic=True)
    assert len(out) > 100
    assert df.read_meta("NONET", str(tmp_path)).get("synthetic") is True


def test_provider_synthetic_requires_explicit_opt_in(tmp_path):
    with pytest.raises(ValueError):
        df.fetch("SYN", provider="synthetic", data_dir=str(tmp_path))
    out = df.fetch("SYN", provider="synthetic", data_dir=str(tmp_path), allow_synthetic=True)
    assert len(out) > 100


# --------------------------------------------------------------------------- #
# aligned_frame(): the multi-asset entry point
# --------------------------------------------------------------------------- #
def test_aligned_frame_restricts_rows_to_where_the_universe_exists():
    a = df.synthetic("A", "2015-01-01", "2019-12-31")
    b = df.synthetic("B", "2017-01-01", "2019-12-31")     # starts two years later
    out = df.aligned_frame({"A": a, "B": b}, field="close", min_coverage=0.95)
    assert list(out.columns) == ["A", "B"]
    assert out.index.min() >= pd.Timestamp("2017-01-01")
    assert out.notna().all().all()

    # with a strict coverage requirement the earlier rows are excluded entirely
    partial = df.aligned_frame({"A": a, "B": b}, field="close", min_coverage=1.0)
    assert partial.index.min() >= pd.Timestamp("2017-01-01")
    assert len(partial) < len(a)
