"""kit/metrics.py - the reference implementation of every number this course uses.

Rules of engagement
-------------------
1. This file is a REFERENCE, not a library you import forever. From Week 3 you
   rebuild these functions in `engine/metrics.py`, and `tests/test_metrics.py`
   compares your version against this one. If your number disagrees with the
   reference, one of you is wrong and it is usually the new code.
2. Every function here is unit-tested in `kit/tests/test_metrics.py`. Run them:
       python -m pytest kit/tests -q
3. Every function either takes a return series or an equity series - never both
   and never "whatever you have". Return series are simple (arithmetic) returns,
   not log returns, unless the name says `log`.
4. Costs are NOT modelled here. Costs enter at the engine level (Week 3-4), as
   cash deductions. A metric that silently adjusts for costs is a lie.

Conventions
-----------
- `returns`: pd.Series indexed by date/time, simple returns (0.01 = +1%).
- `equity`:  pd.Series indexed by date/time, a cumulative value (start anywhere,
  normally 1.0 or 100_000).
- Frequencies are inferred from the index unless `periods_per_year` is passed.

Quick reference:  metrics.sharpe(r) -> float,  metrics.tearsheet(equity) -> str
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, Mapping, Optional, Sequence, Union

import numpy as np
import pandas as pd

SeriesLike = Union[pd.Series, Sequence[float], np.ndarray]


# --------------------------------------------------------------------------- #
# plumbing
# --------------------------------------------------------------------------- #
def _as_series(x: SeriesLike, name: str = "x") -> pd.Series:
    if isinstance(x, pd.Series):
        out = x.astype(float)
        out.name = x.name or name
        return out
    return pd.Series(np.asarray(x, dtype=float), name=name)


def periods_per_year(index: Optional[pd.Index], override: Optional[float] = None) -> float:
    """Infer bars per year from the index spacing. Never guess when you can measure."""
    if override is not None:
        return float(override)
    if index is None or len(index) < 3:
        return 252.0
    idx = pd.Index(index)
    if not isinstance(idx, pd.DatetimeIndex):
        return 252.0
    naive = idx.tz_convert("UTC").tz_localize(None) if idx.tz is not None else idx
    diffs = np.diff(naive.to_numpy().astype("datetime64[D]").astype("int64")).astype(float)
    if len(diffs) == 0:
        return 252.0
    median_days = float(np.median(diffs[diffs > 0])) if np.any(diffs > 0) else 1.0
    if median_days <= 1.5:
        return 252.0
    if median_days <= 9:
        return 52.0
    if median_days <= 45:
        return 12.0
    return 1.0


def to_returns(equity: SeriesLike) -> pd.Series:
    """Equity -> simple returns. The first bar is dropped (you cannot return from nothing)."""
    eq = _as_series(equity, "equity")
    out = eq / eq.shift(1) - 1.0
    return out.iloc[1:].dropna()


def to_equity(returns: SeriesLike, initial: float = 1.0) -> pd.Series:
    r = _as_series(returns, "returns").fillna(0.0)
    return initial * (1.0 + r).cumprod()


# --------------------------------------------------------------------------- #
# return and risk: level 1
# --------------------------------------------------------------------------- #
def total_return(returns: SeriesLike) -> float:
    r = _as_series(returns, "returns").dropna()
    if len(r) == 0:
        return 0.0
    return float((1.0 + r).prod() - 1.0)


def cagr(returns: SeriesLike, index: Optional[pd.Index] = None, ppy: Optional[float] = None) -> float:
    """Compound annual growth rate from a return series."""
    r = _as_series(returns, "returns").dropna()
    idx = index if index is not None else r.index
    if len(r) == 0:
        return 0.0
    n_years = len(r) / periods_per_year(idx, ppy)
    growth = 1.0 + total_return(r)
    if growth <= 0:
        return -1.0
    return float(growth ** (1.0 / n_years) - 1.0) if n_years > 0 else 0.0


def ann_return(returns: SeriesLike, index: Optional[pd.Index] = None, ppy: Optional[float] = None) -> float:
    """Arithmetic annualised mean return. Used by Sharpe; prefer cagr for reporting."""
    r = _as_series(returns, "returns").dropna()
    idx = index if index is not None else r.index
    if len(r) == 0:
        return 0.0
    return float(r.mean() * periods_per_year(idx, ppy))


def vol(returns: SeriesLike, index: Optional[pd.Index] = None, ppy: Optional[float] = None) -> float:
    """Annualised standard deviation of returns (sample std, ddof=1)."""
    r = _as_series(returns, "returns").dropna()
    idx = index if index is not None else r.index
    if len(r) < 2:
        return 0.0
    return float(r.std(ddof=1) * math.sqrt(periods_per_year(idx, ppy)))


def downside_deviation(
    returns: SeriesLike,
    mar: float = 0.0,
    index: Optional[pd.Index] = None,
    ppy: Optional[float] = None,
) -> float:
    """Annualised deviation of returns below the minimum acceptable return (default 0)."""
    r = _as_series(returns, "returns").dropna()
    idx = index if index is not None else r.index
    if len(r) < 2:
        return 0.0
    shortfall = np.minimum(r.values - mar, 0.0)
    dd = math.sqrt(float(np.mean(shortfall ** 2)))
    return float(dd * math.sqrt(periods_per_year(idx, ppy)))


def sharpe(
    returns: SeriesLike,
    rf: float = 0.0,
    index: Optional[pd.Index] = None,
    ppy: Optional[float] = None,
) -> float:
    """(annualised excess return) / (annualised vol). rf is an ANNUAL rate."""
    r = _as_series(returns, "returns").dropna()
    idx = index if index is not None else r.index
    ppy_val = periods_per_year(idx, ppy)
    if len(r) < 2:
        return 0.0
    excess = r - rf / ppy_val
    sd = excess.std(ddof=1)
    if not np.isfinite(sd) or sd < 1e-12:
        return 0.0
    return float(math.sqrt(ppy_val) * excess.mean() / sd)


def sortino(
    returns: SeriesLike,
    mar: float = 0.0,
    index: Optional[pd.Index] = None,
    ppy: Optional[float] = None,
) -> float:
    """Like Sharpe but only punishes downside. mar is an ANNUAL rate."""
    r = _as_series(returns, "returns").dropna()
    idx = index if index is not None else r.index
    ppy_val = periods_per_year(idx, ppy)
    dd = downside_deviation(r, mar / ppy_val, idx, ppy_val)
    excess = r.mean() * ppy_val - mar
    if dd < 1e-12:
        # No downside at all: the ratio is infinite. Return inf rather than a
        # pretty finite number - a strategy that never lost is a red flag, not a 99.
        return float("inf") if excess > 0 else 0.0
    return float(excess / dd)


# --------------------------------------------------------------------------- #
# drawdown
# --------------------------------------------------------------------------- #
def drawdown_series(equity: SeriesLike) -> pd.Series:
    """Percentage below the running peak. Always <= 0."""
    eq = _as_series(equity, "equity")
    peak = eq.cummax()
    return eq / peak - 1.0


def max_drawdown(equity: SeriesLike) -> float:
    """Worst peak-to-trough decline as a negative number (-0.47 = -47%)."""
    dd = drawdown_series(equity)
    return float(dd.min()) if len(dd) else 0.0


def max_drawdown_duration(equity: SeriesLike) -> int:
    """Longest run of bars spent below a previous peak (bars, not days)."""
    dd = drawdown_series(equity)
    longest = current = 0
    for value in dd.values:
        current = current + 1 if value < 0 else 0
        longest = max(longest, current)
    return int(longest)


def time_to_recovery(equity: SeriesLike) -> int:
    """Bars from the max-drawdown trough until the old peak is regained (0 = never, within the sample)."""
    eq = _as_series(equity, "equity")
    if len(eq) == 0:
        return 0
    dd = drawdown_series(eq)
    trough_pos = int(eq.index.get_loc(dd.idxmin()))
    peak_value = float(eq.cummax().iloc[trough_pos])
    after = eq.iloc[trough_pos:]
    recovered = after[after >= peak_value]
    if len(recovered) == 0:
        return 0
    recovery_pos = int(eq.index.get_loc(recovered.index[0]))
    return recovery_pos - trough_pos


def ulcer_index(equity: SeriesLike) -> float:
    """Root-mean-square drawdown: how much pain, not just how deep."""
    dd = drawdown_series(equity)
    if len(dd) == 0:
        return 0.0
    return float(math.sqrt((dd.values ** 2).mean()))


def calmar(returns: SeriesLike, equity: Optional[SeriesLike] = None, index: Optional[pd.Index] = None) -> float:
    """CAGR / |MaxDD|. 'Return per unit of worst pain'."""
    r = _as_series(returns, "returns").dropna()
    eq = _as_series(equity, "equity") if equity is not None else to_equity(r)
    mdd = abs(max_drawdown(eq))
    if mdd == 0:
        return 0.0
    return float(cagr(r, index) / mdd)


def recovery_factor(returns: SeriesLike, equity: Optional[SeriesLike] = None) -> float:
    """Total return / |MaxDD| - how many times over the strategy paid for its worst wound."""
    r = _as_series(returns, "returns").dropna()
    eq = _as_series(equity, "equity") if equity is not None else to_equity(r)
    mdd = abs(max_drawdown(eq))
    if mdd == 0:
        return 0.0
    return float(total_return(r) / mdd)


# --------------------------------------------------------------------------- #
# tail risk
# --------------------------------------------------------------------------- #
def value_at_risk(returns: SeriesLike, level: float = 0.05) -> float:
    """Historical VaR: the `level` quantile of the return distribution (negative number)."""
    r = _as_series(returns, "returns").dropna()
    if len(r) == 0:
        return 0.0
    return float(np.quantile(r.values, level))


def cvar(returns: SeriesLike, level: float = 0.05) -> float:
    """Expected shortfall: mean of returns at or below the VaR quantile."""
    r = _as_series(returns, "returns").dropna()
    if len(r) == 0:
        return 0.0
    threshold = value_at_risk(r, level)
    tail = r[r <= threshold]
    if len(tail) == 0:
        return float(threshold)
    return float(tail.mean())


# --------------------------------------------------------------------------- #
# trade-level statistics (this is where "90% win rate" lives)
# --------------------------------------------------------------------------- #
def _pnl_array(trades: Union[pd.DataFrame, SeriesLike]) -> np.ndarray:
    if isinstance(trades, pd.DataFrame):
        for column in ("pnl", "net_pnl", "profit"):
            if column in trades.columns:
                return trades[column].astype(float).dropna().values
        raise KeyError("trades DataFrame needs a 'pnl' column (net of costs)")
    return _as_series(trades, "pnl").dropna().values


def win_rate(trades: Union[pd.DataFrame, SeriesLike]) -> float:
    pnl = _pnl_array(trades)
    if len(pnl) == 0:
        return 0.0
    return float((pnl > 0).mean())


def expectancy(trades: Union[pd.DataFrame, SeriesLike], notional: float = 1.0) -> float:
    """Average profit per trade. THE number that matters.

    expectancy = win_rate * avg_win - loss_rate * avg_loss

    `notional` lets you express it as a fraction of capital per trade; leave 1.0
    for currency, pass your per-trade capital for a percentage.
    """
    pnl = _pnl_array(trades)
    if len(pnl) == 0:
        return 0.0
    return float(pnl.mean() / notional)


def profit_factor(trades: Union[pd.DataFrame, SeriesLike]) -> float:
    """Gross profits / gross losses. 1.0 = breakeven before costs. <1.0 = a donation."""
    pnl = _pnl_array(trades)
    if len(pnl) == 0:
        return 0.0
    gross_win = float(pnl[pnl > 0].sum())
    gross_loss = float(-pnl[pnl < 0].sum())
    if gross_loss == 0:
        return float("inf") if gross_win > 0 else 0.0
    return gross_win / gross_loss


def payoff_ratio(trades: Union[pd.DataFrame, SeriesLike]) -> float:
    """Average win size / average loss size."""
    pnl = _pnl_array(trades)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    if len(wins) == 0 or len(losses) == 0:
        return 0.0
    return float(wins.mean() / abs(losses.mean()))


def breakeven_win_rate(trades: Union[pd.DataFrame, SeriesLike]) -> float:
    """The win rate you would need for expectancy to be exactly zero.

    If a strategy claims 90% win rate and this prints 0.94, the strategy is a
    loss machine with pretty stats.
    """
    pnl = _pnl_array(trades)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    if len(wins) == 0 or len(losses) == 0:
        return float("nan")
    avg_win, avg_loss = wins.mean(), abs(losses.mean())
    return float(avg_loss / (avg_win + avg_loss))


def streaks(trades: Union[pd.DataFrame, SeriesLike]) -> Dict[str, int]:
    pnl = _pnl_array(trades)
    best_w = best_l = cur_w = cur_l = 0
    for value in pnl:
        cur_w = cur_w + 1 if value > 0 else 0
        cur_l = cur_l + 1 if value < 0 else 0
        best_w, best_l = max(best_w, cur_w), max(best_l, cur_l)
    return {"max_win_streak": int(best_w), "max_loss_streak": int(best_l)}


def trade_stats(trades: Union[pd.DataFrame, SeriesLike], notional: float = 1.0) -> Dict[str, float]:
    """Everything above, in one dict. This is what feeds your verdict template."""
    pnl = _pnl_array(trades)
    stats = {
        "n_trades": float(len(pnl)),
        "total_pnl": float(pnl.sum()) if len(pnl) else 0.0,
        "win_rate": win_rate(pnl),
        "expectancy": expectancy(pnl, notional),
        "profit_factor": profit_factor(pnl),
        "payoff_ratio": payoff_ratio(pnl),
        "breakeven_win_rate": breakeven_win_rate(pnl),
    }
    stats.update({k: float(v) for k, v in streaks(pnl).items()})
    return stats


# --------------------------------------------------------------------------- #
# the one function you call to describe a backtest
# --------------------------------------------------------------------------- #
def summary(result_or_equity, trades: Optional[pd.DataFrame] = None, rf: float = 0.0, ppy: Optional[float] = None) -> Dict[str, float]:
    """Metric dict for anything with `.equity`/`.returns`, or for a bare equity series."""
    if hasattr(result_or_equity, "equity"):
        equity = _as_series(getattr(result_or_equity, "equity"), "equity")
        trades = trades if trades is not None else getattr(result_or_equity, "trades", None)
    else:
        equity = _as_series(result_or_equity, "equity")
    returns = to_returns(equity)
    out = {
        "n_bars": float(len(returns)),
        "total_return": total_return(returns),
        "cagr": cagr(returns, equity.index, ppy),
        "ann_vol": vol(returns, equity.index, ppy),
        "sharpe": sharpe(returns, rf, equity.index, ppy),
        "sortino": sortino(returns, 0.0, equity.index, ppy),
        "max_drawdown": max_drawdown(equity),
        "max_dd_duration": float(max_drawdown_duration(equity)),
        "calmar": calmar(returns, equity, equity.index),
        "ulcer_index": ulcer_index(equity),
        "var_95": value_at_risk(returns, 0.05),
        "cvar_95": cvar(returns, 0.05),
        "skew": float(returns.skew()) if len(returns) > 2 else 0.0,
        "kurtosis": float(returns.kurtosis()) if len(returns) > 3 else 0.0,
    }
    if trades is not None and len(trades) > 0:
        out.update(trade_stats(trades))
    return {k: (float(v) if not isinstance(v, float) else v) for k, v in out.items()}


FORMATS = {
    "n_bars": "{:.0f}",
    "n_trades": "{:.0f}",
    "total_return": "{:+.2%}",
    "cagr": "{:+.2%}",
    "ann_vol": "{:.2%}",
    "sharpe": "{:.2f}",
    "sortino": "{:.2f}",
    "max_drawdown": "{:.2%}",
    "max_dd_duration": "{:.0f}",
    "calmar": "{:.2f}",
    "ulcer_index": "{:.2%}",
    "var_95": "{:.2%}",
    "cvar_95": "{:.2%}",
    "skew": "{:+.2f}",
    "kurtosis": "{:+.2f}",
    "total_pnl": "{:,.0f}",
    "win_rate": "{:.1%}",
    "expectancy": "{:+.4f}",
    "profit_factor": "{:.2f}",
    "payoff_ratio": "{:.2f}",
    "breakeven_win_rate": "{:.1%}",
    "max_win_streak": "{:.0f}",
    "max_loss_streak": "{:.0f}",
}


def format_metric(name: str, value: float) -> str:
    fmt = FORMATS.get(name)
    if fmt is None or value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    try:
        return fmt.format(value)
    except (ValueError, TypeError):
        return str(value)


def tearsheet(metrics: Mapping[str, float], title: str = "Backtest tearsheet") -> str:
    """Markdown tearsheet from a metrics dict. Week 3/4 rebuilds this as a generator."""
    groups = [
        ("Returns", ["n_bars", "total_return", "cagr", "ann_vol"]),
        ("Risk-adjusted", ["sharpe", "sortino", "calmar", "ulcer_index"]),
        ("Drawdown", ["max_drawdown", "max_dd_duration", "var_95", "cvar_95"]),
        ("Tails", ["skew", "kurtosis"]),
        ("Trades", ["n_trades", "total_pnl", "win_rate", "expectancy", "profit_factor", "payoff_ratio", "breakeven_win_rate", "max_loss_streak"]),
    ]
    lines = ["## %s" % title, ""]
    for group, keys in groups:
        present = [k for k in keys if k in metrics]
        if not present:
            continue
        lines.append("**%s**" % group)
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("| --- | --- |")
        for key in present:
            lines.append("| `%s` | %s |" % (key, format_metric(key, metrics[key])))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def cost_drag_summary(gross_returns: SeriesLike, net_returns: SeriesLike) -> Dict[str, float]:
    """How much of the strategy is the strategy, and how much is the toll booth."""
    g = _as_series(gross_returns, "gross")
    n = _as_series(net_returns, "net")
    return {
        "gross_total_return": total_return(g),
        "net_total_return": total_return(n),
        "cost_drag_total": total_return(g) - total_return(n),
        "cost_drag_annualised": (g.mean() - n.mean()) * periods_per_year(g.index),
        "sharpe_gross": sharpe(g),
        "sharpe_net": sharpe(n),
    }
