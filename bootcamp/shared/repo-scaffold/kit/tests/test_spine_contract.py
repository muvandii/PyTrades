"""kit/tests/test_spine_contract.py - the contract your own engine must satisfy.

Run against the reference backtester (default):
    python -m pytest kit/tests/test_spine_contract.py -q

Run against YOUR engine (Week 4 onwards, after you build engine/backtest.py):
    PYTRADES_ENGINE=engine.backtest python -m pytest kit/tests/test_spine_contract.py -q

Your engine passes when all of these pass unchanged. This is the mechanical
half of Deliverable D07 and one of the Week 4 gate checks. No network needed:
every price frame here is built in the test.

The contract in one sentence: `run_backtest(spec, prices=..., signals=...)`
must accept target weights in [-1, 1] decided at bar t, fill them at bar t+1,
charge costs on |change in weight|, and return an object with `.equity`,
`.returns`, `.positions`, `.trades`, `.metrics`, `.state_at()`, `.save()`,
`.load()`.
"""

from __future__ import annotations

import importlib
import inspect
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

ENGINE_NAME = os.environ.get("PYTRADES_ENGINE", "kit.spine")
E = importlib.import_module(ENGINE_NAME)


# --------------------------------------------------------------------------- #
# fixtures built in-test: no network, fully deterministic
# --------------------------------------------------------------------------- #
def make_prices(n: int = 300, seed: int = 11, drift: float = 0.0003, sigma: float = 0.01) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    index = pd.bdate_range("2020-01-01", periods=n)
    close = 100.0 * np.exp(np.cumsum(rng.normal(drift, sigma, n)))
    open_ = close * (1 + rng.normal(0, sigma / 4, n))
    high = np.maximum(close, open_) * (1 + np.abs(rng.normal(0, sigma / 6, n)))
    low = np.minimum(close, open_) * (1 - np.abs(rng.normal(0, sigma / 6, n)))
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": 1e6}, index=index)


def trending_prices(legs=(60, 60, 60, 60), step: float = 0.01) -> pd.DataFrame:
    """A perfectly trending market: legs of +1%/bar, then -1%/bar, alternating."""
    closes = [100.0]
    for i, length in enumerate(legs):
        direction = 1.0 if i % 2 == 0 else -1.0
        for _ in range(length):
            closes.append(closes[-1] * (1.0 + direction * step))
    index = pd.bdate_range("2020-01-01", periods=len(closes))
    close = pd.Series(closes, index=index)
    return pd.DataFrame({"open": close, "high": close, "low": close, "close": close, "volume": 1e6})


def spec(**overrides):
    base = dict(id="T", name="contract test", universe=["SPY"], params={}, long_only=False, max_gross_exposure=1.0)
    base.update(overrides)
    return E.StrategySpec(**base)


def constant_signal(index, value=1.0):
    return pd.DataFrame({"SPY": value}, index=index)


def momentum_signal(prices: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    close = prices["close"]
    return pd.DataFrame({"SPY": np.sign(close / close.shift(lookback) - 1.0).fillna(0.0)}, index=prices.index)


# --------------------------------------------------------------------------- #
# alignment: the whole point
# --------------------------------------------------------------------------- #
def test_signal_is_executed_one_bar_later():
    prices = make_prices()
    signal = pd.DataFrame({"SPY": 0.0}, index=prices.index)
    signal.iloc[100:] = 1.0
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal)
    positions = result.positions["SPY"]
    assert positions.iloc[99] == 0.0, "position appeared before the signal existed"
    assert positions.iloc[100] == 0.0, "position appeared on the decision bar (look-ahead!)"
    assert positions.iloc[101] == 1.0, "position did not appear on the bar after the decision"


def test_lookahead_premium_is_real_and_positive():
    """signal_shift=0 is cheating. The cheat must show up as a better result."""
    prices = trending_prices()
    signal = momentum_signal(prices, lookback=20)
    honest = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal, signal_shift=1)
    cheating = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal, signal_shift=0)
    assert cheating.metrics["total_return"] > honest.metrics["total_return"]
    assert cheating.metrics["sharpe"] > honest.metrics["sharpe"]


def test_equity_starts_at_initial_capital():
    prices = make_prices()
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=constant_signal(prices.index), initial_capital=50_000.0)
    assert result.equity.iloc[0] == pytest.approx(50_000.0)
    assert len(result.equity) == len(prices)


def test_constant_full_weight_replicates_buy_and_hold():
    """With next_close execution, weight 1.0 must BE the asset's return, exactly."""
    prices = make_prices()
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=constant_signal(prices.index), execution="next_close")
    price_ratio = prices["close"].iloc[-1] / prices["close"].iloc[0]
    equity_ratio = result.equity.iloc[-1] / result.equity.iloc[0]
    assert equity_ratio == pytest.approx(price_ratio, rel=1e-9)


def test_next_open_attributes_the_overnight_gap_to_the_position_held_into_the_bar():
    """The two legs of a next_open bar, pinned.

    Bar t's return is the overnight gap (held by target[t-1], the position filled at
    the previous bar's open) plus the intraday move (filled at bar t's open by
    target[t], i.e. the decision from bar t-1's close). Construct a gap-only market -
    open[t] == close[t] - so the intraday leg is exactly zero and the equity curve
    isolates the overnight attribution.
    """
    rng = np.random.default_rng(5)
    n = 200
    index = pd.bdate_range("2020-01-01", periods=n)
    gaps = rng.normal(0.001, 0.01, n)
    closes = 100.0 * np.cumprod(1.0 + gaps)
    prices = pd.DataFrame(
        {"open": closes, "high": closes, "low": closes, "close": closes, "volume": 1e6},  # open == close
        index=index,
    )
    signal = constant_signal(index, 1.0)
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal, execution="next_open")

    expected = float(np.cumprod(1.0 + pd.Series(gaps, index=index).iloc[2:].to_numpy())[-1])
    actual = result.equity.iloc[-1] / result.equity.iloc[0]
    assert actual == pytest.approx(expected, rel=1e-9), (
        "overnight attribution is off by a bar: expected the gap series to start at bar 2 "
        "(bar 0 is unfilled, bar 1's gap is not yet held)"
    )
    assert result.returns.iloc[1] == pytest.approx(0.0)


# --------------------------------------------------------------------------- #
# costs
# --------------------------------------------------------------------------- #
def test_costs_reduce_returns_monotonically_in_bps():
    prices = make_prices()
    signal = momentum_signal(prices, lookback=5)  # chatty signal: lots of turnover
    totals = []
    for bps in (0.0, 5.0, 10.0, 25.0):
        result = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal, fee_bps=bps, slippage_bps=bps)
        totals.append(result.metrics["total_return"])
    assert totals == sorted(totals, reverse=True), "more cost must mean less return: %s" % totals
    assert totals[0] > totals[-1]


def test_zero_cost_run_reports_zero_cost_drag():
    prices = make_prices()
    signal = momentum_signal(prices, lookback=5)
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal)
    assert abs(result.meta.get("total_cost_drag", 0.0)) < 1e-12


def test_turnover_is_charged_on_weight_changes():
    """One flip from flat to full and back must cost roughly 2 x weight x rate."""
    prices = make_prices(120)
    signal = pd.DataFrame({"SPY": 0.0}, index=prices.index)
    signal.iloc[40:] = 1.0
    free = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal, fee_bps=0.0)
    costly = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal, fee_bps=100.0)  # 1% per unit turnover
    drag = free.metrics["total_return"] - costly.metrics["total_return"]
    assert 0.01 < drag < 0.06, "two-way turnover of 100%% at 1%% should cost ~2%%, got %.4f" % drag


# --------------------------------------------------------------------------- #
# signal validation: fail loudly, not silently
# --------------------------------------------------------------------------- #
def test_all_nan_signal_is_rejected():
    prices = make_prices(60)
    signal = pd.DataFrame({"SPY": np.nan}, index=prices.index)
    with pytest.raises(Exception):
        _run_with_signal_generation(signal)


def test_leveraged_weights_are_rejected():
    prices = make_prices(60)
    signal = pd.DataFrame({"SPY": 3.0}, index=prices.index)
    with pytest.raises(Exception):
        _run_with_signal_generation(signal)


def test_long_only_spec_rejects_short_signals():
    prices = make_prices(60)
    signal = pd.DataFrame({"SPY": -1.0}, index=prices.index)
    with pytest.raises(Exception):
        _run_with_signal_generation(signal, long_only=True)


def _run_with_signal_generation(signal, **spec_overrides):
    """Feed a signal through the same validation path a real strategy would take.

    We monkeypatch the engine's signal loader so the test does not need a file
    on disk, but we do NOT skip validation.
    """
    prices = make_prices(len(signal))
    signal.index = prices.index

    class _Fake:
        pass

    if hasattr(E, "build_signals"):
        original = E.load_signal_function if hasattr(E, "load_signal_function") else None
        try:
            if original is not None:
                E.load_signal_function = lambda path: (lambda p, params: signal)
                return E.run_backtest(spec(**spec_overrides), prices={"SPY": prices})
        finally:
            if original is not None:
                E.load_signal_function = original
    # engines that do not expose build_signals still must reject bad weights
    return E.run_backtest(spec(**spec_overrides), prices={"SPY": prices}, signals=signal)


# --------------------------------------------------------------------------- #
# trades, persistence, state
# --------------------------------------------------------------------------- #
def test_extract_trades_counts_round_trips():
    if not hasattr(E, "extract_trades"):
        pytest.skip("%s does not expose extract_trades" % ENGINE_NAME)
    index = pd.bdate_range("2020-01-01", periods=10)
    positions = pd.DataFrame({"SPY": [0, 1, 1, 0, 0, -1, 0, 1, 1, 1]}, index=index, dtype=float)
    returns = pd.DataFrame({"SPY": np.zeros(10)}, index=index)
    equity = pd.Series(np.linspace(100_000, 110_000, 10), index=index)
    trades = E.extract_trades(positions, returns, equity, 0.0)
    assert len(trades) == 3, "expected 3 round trips (long, short, then an open long), got %d" % len(trades)
    assert list(trades["side"]) == ["long", "short", "long"]
    assert trades["bars_held"].sum() == 2 + 1 + 2


def test_save_load_round_trip(tmp_path):
    prices = make_prices()
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=constant_signal(prices.index), name="roundtrip")
    out_dir = result.save(directory=str(tmp_path / "roundtrip"))
    assert os.path.exists(os.path.join(out_dir, "equity.csv"))
    assert os.path.exists(os.path.join(out_dir, "meta.json"))
    loaded = E.BacktestResult.load(out_dir)
    assert loaded.metrics["sharpe"] == pytest.approx(result.metrics["sharpe"], rel=1e-9)
    assert loaded.metrics["total_return"] == pytest.approx(result.metrics["total_return"], rel=1e-9)
    assert len(loaded.trades) == len(result.trades)


def test_meta_records_provenance():
    prices = make_prices()
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=constant_signal(prices.index), fee_bps=2.0, slippage_bps=3.0)
    meta = result.meta
    for key in ("data_fingerprint", "spec_fingerprint", "created_at", "fee_bps", "slippage_bps", "bars"):
        assert key in meta, "meta is missing %s - verdicts must be reproducible" % key
    assert meta["fee_bps"] == 2.0 and meta["slippage_bps"] == 3.0


def test_state_at_returns_positions_for_a_past_bar():
    prices = make_prices(200)
    signal = constant_signal(prices.index)
    result = E.run_backtest(spec(), prices={"SPY": prices}, signals=signal)
    state = result.state_at(prices.index[100])
    assert state["positions"]["SPY"] == pytest.approx(1.0)
    assert state["equity"] > 0


def test_fingerprint_changes_when_the_signal_code_changes(tmp_path):
    if not hasattr(E, "StrategySpec"):
        pytest.skip("engine has no StrategySpec")
    strategy_dir = tmp_path / "strategies" / "FP"
    strategy_dir.mkdir(parents=True)
    (strategy_dir / "signal.py").write_text("def generate(prices, params):\n    return None\n")
    os.chdir(tmp_path)
    first = E.StrategySpec(id="FP", name="fp", universe=["SPY"], params={"a": 1}).fingerprint()
    (strategy_dir / "signal.py").write_text("def generate(prices, params):\n    return 1\n")
    second = E.StrategySpec(id="FP", name="fp", universe=["SPY"], params={"a": 1}).fingerprint()
    third = E.StrategySpec(id="FP", name="fp", universe=["SPY"], params={"a": 2}).fingerprint()
    assert first != second, "changing signal code must change the fingerprint"
    assert second != third, "changing params must change the fingerprint"


def test_rebalance_holds_between_decisions():
    if not hasattr(E, "apply_rebalance"):
        pytest.skip("%s does not expose apply_rebalance" % ENGINE_NAME)
    index = pd.bdate_range("2024-01-01", periods=15)
    raw = pd.DataFrame({"SPY": np.arange(15, dtype=float)}, index=index)
    held = E.apply_rebalance(raw, "weekly")["SPY"]
    # 2024-01-01 is a Monday: decisions land on Fridays (idx 4 = Jan 5, idx 9 = Jan 12)
    assert held.iloc[0] == 0.0, "there is no decision yet, so the target must be flat"
    assert held.iloc[4] == 4.0, "the weekly decision was not taken on the last bar of the week"
    assert held.iloc[5] == held.iloc[8] == 4.0, "the weekly target was not held between decisions"
    assert held.iloc[9] == 9.0, "the next weekly decision did not update the target"
    assert len(held) == len(raw)


def test_engine_accepts_the_documented_signature():
    """Week 4 gate: your engine must have the same call surface as the spine."""
    signature = inspect.signature(E.run_backtest)
    for parameter in ("spec", "prices", "signals", "initial_capital", "fee_bps", "slippage_bps", "execution"):
        assert parameter in signature.parameters, "run_backtest() is missing parameter %r" % parameter
    import dataclasses

    fields = {f.name for f in dataclasses.fields(E.BacktestResult)}
    assert {"equity", "returns", "positions", "trades", "meta"} <= fields, "BacktestResult is missing fields: %s" % fields
    for method in ("save", "load", "state_at"):
        assert hasattr(E.BacktestResult, method), "BacktestResult is missing %s()" % method
