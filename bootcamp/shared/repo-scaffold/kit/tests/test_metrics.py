"""kit/tests/test_metrics.py - hand-computed truths for every metric.

Run:  python -m pytest kit/tests/test_metrics.py -q

These tests use tiny series small enough to verify on paper. If a test fails,
your metric is wrong - not the test. This file is the oracle that
`tests/test_metrics.py` (your Week 3 rebuild) is compared against.
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kit import metrics as m  # noqa: E402


def daily_index(n: int, start: str = "2020-01-01") -> pd.DatetimeIndex:
    return pd.bdate_range(start, periods=n)


# --------------------------------------------------------------------------- #
# returns and compounding
# --------------------------------------------------------------------------- #
def test_to_returns_and_back():
    equity = pd.Series([100.0, 110.0, 99.0], index=daily_index(3))
    returns = m.to_returns(equity)
    assert len(returns) == 2
    assert math.isclose(returns.iloc[0], 0.10, rel_tol=1e-12)
    assert math.isclose(returns.iloc[1], -0.10, rel_tol=1e-12)


def test_total_return_is_multiplicative_not_additive():
    returns = pd.Series([0.10, -0.10])
    assert math.isclose(m.total_return(returns), -0.01, rel_tol=1e-12)
    # the naive sum says 0%; compounding says -1%. Compounding wins.


def test_to_equity_round_trip():
    """An equity curve has one more bar than its return series - the first return is gone."""
    returns = pd.Series([0.05, -0.02, 0.03], index=daily_index(3))
    equity = m.to_equity(returns, 100.0)
    assert len(equity) == len(returns)
    assert math.isclose(m.to_equity(returns, 100.0).iloc[-1], 105.987, rel_tol=1e-9)
    round_trip = m.to_returns(equity)
    assert len(round_trip) == len(returns) - 1
    assert np.allclose(round_trip.values, returns.values[1:])


def test_cagr_one_year_of_01_percent_days():
    returns = pd.Series(np.full(252, 0.001), index=daily_index(252))
    expected = 1.001 ** 252 - 1
    assert math.isclose(m.cagr(returns), expected, rel_tol=1e-9)


def test_periods_per_year_inference():
    assert m.periods_per_year(daily_index(100)) == 252.0
    assert m.periods_per_year(pd.date_range("2020-01-01", periods=30, freq="W-FRI")) == 52.0
    assert m.periods_per_year(pd.date_range("2020-01-01", periods=30, freq="ME")) == 12.0
    assert m.periods_per_year(None) == 252.0


# --------------------------------------------------------------------------- #
# risk
# --------------------------------------------------------------------------- #
def test_vol_of_constant_returns_is_zero():
    returns = pd.Series(np.full(50, 0.002), index=daily_index(50))
    assert m.vol(returns) == 0.0


def test_sharpe_matches_definition():
    rng = np.random.default_rng(0)
    returns = pd.Series(rng.normal(0.0005, 0.01, 500), index=daily_index(500))
    expected = math.sqrt(252) * returns.mean() / returns.std(ddof=1)
    assert math.isclose(m.sharpe(returns), expected, rel_tol=1e-12)


def test_sharpe_of_zero_vol_is_zero_not_infinity():
    assert m.sharpe(pd.Series(np.full(100, 0.001))) == 0.0


def test_downside_deviation_ignores_upside():
    modest_upside = pd.Series([0.05, -0.01, 0.02, -0.01], index=daily_index(4))
    huge_upside = pd.Series([0.90, -0.01, 0.75, -0.01], index=daily_index(4))
    assert math.isclose(m.downside_deviation(modest_upside), m.downside_deviation(huge_upside), rel_tol=1e-12)
    assert m.vol(huge_upside) > m.vol(modest_upside)


def test_sortino_beats_sharpe_when_upside_is_lumpy():
    """Lumpy gains inflate std (hurting Sharpe) without inflating downside deviation."""
    returns = pd.Series(np.full(400, 0.0005), index=daily_index(400))
    returns.iloc[::20] = 0.05    # 20 fat gains
    returns.iloc[::50] = -0.0002  # a sliver of downside so the ratio stays finite
    assert m.sortino(returns) > m.sharpe(returns)


def test_infinite_sortino_is_flagged_not_prettified():
    returns = pd.Series(np.full(100, 0.001), index=daily_index(100))
    assert m.sortino(returns) == float("inf")


def test_max_drawdown_hand_computed():
    equity = pd.Series([1.0, 1.2, 0.6, 1.3], index=daily_index(4))
    assert math.isclose(m.max_drawdown(equity), -0.5, rel_tol=1e-12)


def test_drawdown_duration_and_ulcer():
    equity = pd.Series([1.0, 1.2, 1.18, 1.1, 0.9, 1.1, 1.25], index=daily_index(7))
    assert m.max_drawdown_duration(equity) == 4
    assert m.ulcer_index(equity) > 0


def test_time_to_recovery():
    equity = pd.Series([1.0, 1.2, 0.9, 1.0, 1.21], index=daily_index(5))
    assert m.time_to_recovery(equity) == 2  # trough at index 2, old peak regained at index 4


def test_calmar_and_recovery_factor():
    equity = pd.Series([1.0, 1.25, 0.9, 1.1], index=daily_index(4))
    returns = m.to_returns(equity)
    assert math.isclose(m.calmar(returns, equity), m.cagr(returns) / 0.28, rel_tol=1e-9)
    assert math.isclose(m.recovery_factor(returns, equity), m.total_return(returns) / 0.28, rel_tol=1e-9)


def test_var_and_cvar_relationship():
    rng = np.random.default_rng(2)
    returns = pd.Series(rng.normal(0, 0.01, 2000), index=daily_index(2000))
    var = m.value_at_risk(returns, 0.05)
    assert var < 0
    assert m.cvar(returns, 0.05) <= var


# --------------------------------------------------------------------------- #
# trades: the "90% win rate" family
# --------------------------------------------------------------------------- #
def test_trade_stats_hand_computed():
    trades = pd.Series([10.0, -5.0, 20.0, -10.0])
    assert math.isclose(m.win_rate(trades), 0.5)
    assert math.isclose(m.expectancy(trades), 3.75)
    assert math.isclose(m.profit_factor(trades), 2.0)
    assert math.isclose(m.payoff_ratio(trades), 2.0)
    assert math.isclose(m.breakeven_win_rate(trades), 1.0 / 3.0, rel_tol=1e-12)


def test_high_win_rate_can_still_lose_money():
    """The Week 2 debunk, as a unit test: 90% wins, negative expectancy."""
    trades = pd.Series([1.0] * 90 + [-15.0] * 10)
    assert math.isclose(m.win_rate(trades), 0.9)
    assert m.expectancy(trades) < 0
    assert m.profit_factor(trades) < 1
    assert m.breakeven_win_rate(trades) > m.win_rate(trades)
    assert m.breakeven_win_rate(trades) > 0.93


def test_streaks():
    trades = pd.Series([1.0, 1.0, -1.0, -1.0, -1.0, 1.0])
    assert m.streaks(trades) == {"max_win_streak": 2, "max_loss_streak": 3}


def test_expectancy_in_fraction_of_capital():
    trades = pd.DataFrame({"pnl": [100.0, -50.0]})
    assert math.isclose(m.expectancy(trades, notional=10_000.0), 0.0025, rel_tol=1e-12)


def test_trade_stats_requires_pnl_column():
    with pytest.raises(KeyError):
        m.trade_stats(pd.DataFrame({"symbol": ["SPY"], "shares": [1]}))


def test_streaks_and_infinity_edges():
    assert m.profit_factor(pd.Series([1.0, 2.0])) == float("inf")
    assert m.profit_factor(pd.Series([-1.0, -2.0])) == 0.0
    assert m.win_rate(pd.Series([], dtype=float)) == 0.0
    assert m.expectancy(pd.Series([], dtype=float)) == 0.0


# --------------------------------------------------------------------------- #
# summary + tearsheet
# --------------------------------------------------------------------------- #
def test_summary_runs_and_formats():
    rng = np.random.default_rng(3)
    equity = pd.Series(100_000 * (1 + pd.Series(rng.normal(0.0003, 0.01, 400), index=daily_index(400))).cumprod())
    stats = m.summary(equity)
    for key in ("cagr", "sharpe", "sortino", "max_drawdown", "calmar", "var_95", "cvar_95"):
        assert key in stats
        assert np.isfinite(stats[key])
    sheet = m.tearsheet(stats, title="unit test")
    assert "sharpe" in sheet and "max_drawdown" in sheet and sheet.startswith("## unit test")


def test_format_metric_handles_nan():
    assert m.format_metric("sharpe", float("nan")) == "n/a"
    assert m.format_metric("total_return", 0.1234) == "+12.34%"
    assert m.format_metric("max_drawdown", -0.5) == "-50.00%"


def test_cost_drag_summary():
    rng = np.random.default_rng(4)
    gross = pd.Series(rng.normal(0.0006, 0.01, 252), index=daily_index(252))
    net = gross - 0.0002
    drag = m.cost_drag_summary(gross, net)
    assert drag["cost_drag_total"] > 0
    assert drag["sharpe_net"] < drag["sharpe_gross"]
