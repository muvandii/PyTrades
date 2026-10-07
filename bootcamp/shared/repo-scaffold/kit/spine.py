"""kit/spine.py - the frozen contract between weeks, specs, backtests and artifacts.

Why this file exists
--------------------
Thirteen weeks of deliverables only compose if they all agree on four things:
where data lives, what a strategy spec looks like, what a backtest result looks
like, and how a result is stored on disk. This module fixes those four things.

It is deliberately a *plain, obvious* reference backtester: weight-based,
next-bar execution, no cleverness. You replace it in Weeks 3-4 with your own
engine (`engine/`), and your engine must satisfy `tests/test_spine_contract.py`
- same inputs, same outputs, same files. Everything built before Week 3 keeps
working because the contract does not move.

The four contracts
------------------
1. DATA    `data/<SYMBOL>.csv` + `data/<SYMBOL>.meta.json`   (kit.data_fetcher)
2. SPEC    `config/<strategy_id>.json` -> kit.spine.StrategySpec
3. SIGNAL  `strategies/<dir>/signal.py::generate(prices, params) -> DataFrame`
           of TARGET WEIGHTS in [-1, 1], decided with data up to and including
           bar t. Execution is the spine's job: it shifts by one bar, always.
4. RESULT  `reports/backtests/<name>/{equity.csv,positions.csv,trades.csv,metrics.json,meta.json}`

Anything that consumes those four contracts does not care which week produced it.

Execution semantics (learn these, they are the exam)
----------------------------------------------------
`signals[t]` is decided using data up to and including bar t's close.

* `execution="next_close"`: the decision is filled at bar t+1's close, so the
  position carried through bar t is `signals[t-1]`. Portfolio return on bar t is
      r_t = sum_i signal_i[t-1] * (close_i[t]/close_i[t-1] - 1)
* `execution="next_open"` (default): filled at bar t's open. The decision made at
  bar t-1's close is therefore the position held through bar t, and bar t's return
  splits into two pieces - which is why your live PnL will not match a
  close-to-close backtest. In terms of the executed target (`target[t] =
  signal[t-1]` under the default `signal_shift=1`):
      r_t = sum_i target_i[t-1] * (open_i[t]/close_i[t-1] - 1)   # overnight: held into the bar
          + sum_i target_i[t]   * (close_i[t]/open_i[t]   - 1)   # intraday: filled at this open
  You capture an overnight gap only if you were already positioned for it
  (target[t-1], decided two closes earlier). Chasing an open costs you the gap;
  that cost shows up in Week 11-12 as live divergence.
* Costs are charged on TURNOVER: `|target_i[t] - target_i[t-1]|` per bar, in bps.
* This reference kit restrikes target weights every bar (weights are targets, not
  positions). A real account holds quantities: between rebalances the weights drift
  with the market, which is what your own `engine/` must model - see
  `spec/engine-spec.md` behaviour 5.

Usage
-----
    python -m kit.spine list
    python -m kit.spine run S01_ma_cross --name baseline
    python -m kit.spine run S01_ma_cross --name with_costs --fee-bps 1 --slippage-bps 2
    python -m kit.spine compare baseline with_costs
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

try:  # works both as `python -m kit.spine` and when imported from inside the package
    from . import metrics as metrics_mod
except ImportError:  # pragma: no cover
    import metrics as metrics_mod  # type: ignore

DATA_DIR = os.environ.get("PYTRADES_DATA", "data")
CONFIG_DIR = os.environ.get("PYTRADES_CONFIG", "config")
RESULTS_DIR = os.environ.get("PYTRADES_RESULTS", "reports/backtests")
INITIAL_CAPITAL = float(os.environ.get("PYTRADES_CAPITAL", "100000"))


# --------------------------------------------------------------------------- #
# 2. SPEC
# --------------------------------------------------------------------------- #
@dataclass
class StrategySpec:
    id: str
    name: str
    universe: List[str]
    params: Dict[str, Any] = field(default_factory=dict)
    thesis: str = ""
    tags: List[str] = field(default_factory=list)
    long_only: bool = True
    signal_file: str = "signal.py"           # relative to strategies/<id>/
    max_gross_exposure: float = 1.0
    rebalance: str = "daily"                 # daily | weekly | monthly

    @property
    def strategy_dir(self) -> str:
        return os.path.join("strategies", self.id)

    @property
    def signal_path(self) -> str:
        return os.path.join(self.strategy_dir, self.signal_file)

    def fingerprint(self) -> str:
        """Hash of the spec AND the signal code: a verdict must know what produced it."""
        payload = json.dumps({"spec": asdict(self), "signal": _read_or_empty(self.signal_path)}, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["fingerprint"] = self.fingerprint()
        return payload


def _read_or_empty(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def spec_path(strategy_id: str) -> str:
    return os.path.join(CONFIG_DIR, "%s.json" % strategy_id)


def load_spec(spec: Any, config_dir: str = CONFIG_DIR) -> StrategySpec:
    """Load a spec from an id, a path, a dict, or pass a StrategySpec straight through."""
    if isinstance(spec, StrategySpec):
        return spec
    if isinstance(spec, dict):
        return StrategySpec(**spec)
    text = str(spec)
    path = text if (os.path.sep in text or text.endswith(".json")) else os.path.join(config_dir, "%s.json" % text)
    if not os.path.exists(path):
        raise FileNotFoundError("no spec at %s - see shared/templates/strategy-config-schema.md" % path)
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    payload.setdefault("name", payload.get("id", "unnamed"))
    return StrategySpec(**payload)


def list_specs(config_dir: str = CONFIG_DIR) -> List[StrategySpec]:
    if not os.path.isdir(config_dir):
        return []
    specs: List[StrategySpec] = []
    for name in sorted(os.listdir(config_dir)):
        if not name.endswith(".json"):
            continue
        try:
            specs.append(load_spec(name, config_dir))
        except TypeError as exc:
            print("skipping %s: %s" % (name, exc), file=sys.stderr)
    return specs


# --------------------------------------------------------------------------- #
# 1. DATA (thin wrappers so the spine never touches the network)
# --------------------------------------------------------------------------- #
def load_prices(symbol: str, start: Optional[str] = None, end: Optional[str] = None, data_dir: str = DATA_DIR) -> pd.DataFrame:
    path = os.path.join(data_dir, "%s.csv" % symbol.upper())
    if not os.path.exists(path):
        raise FileNotFoundError("no data for %s - run: python -m kit.data_fetcher fetch %s" % (symbol, symbol))
    frame = pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()
    if start:
        frame = frame[frame.index >= pd.Timestamp(start)]
    if end:
        frame = frame[frame.index <= pd.Timestamp(end)]
    return frame


def load_universe(
    symbols: Sequence[str], start: Optional[str] = None, end: Optional[str] = None, data_dir: str = DATA_DIR
) -> Dict[str, pd.DataFrame]:
    return {symbol: load_prices(symbol, start, end, data_dir) for symbol in symbols}


def close_frame(prices: Dict[str, pd.DataFrame], min_coverage: float = 0.95) -> pd.DataFrame:
    wide = pd.DataFrame({symbol: frame["close"] for symbol, frame in prices.items()})
    coverage = wide.notna().mean(axis=1)
    return wide[coverage >= min_coverage].ffill().dropna(how="all")


def data_fingerprint(symbols: Sequence[str], data_dir: str = DATA_DIR) -> str:
    """Hash of the exact data files used. Two runs with different hashes are different experiments."""
    digest = hashlib.sha256()
    for symbol in sorted(symbols):
        digest.update(symbol.encode())
        digest.update(_read_or_empty(os.path.join(data_dir, "%s.csv" % symbol.upper())).encode("utf-8"))
    return digest.hexdigest()[:16]


# --------------------------------------------------------------------------- #
# 3. SIGNAL
# --------------------------------------------------------------------------- #
def load_signal_function(path: str) -> Callable[..., pd.DataFrame]:
    if not os.path.exists(path):
        raise FileNotFoundError("no signal file at %s" % path)
    module_spec = importlib.util.spec_from_file_location("signal_%s" % abs(hash(path)), path)
    if module_spec is None or module_spec.loader is None:
        raise ImportError("cannot load %s" % path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    if not hasattr(module, "generate"):
        raise AttributeError("%s must define generate(prices, params) -> DataFrame" % path)
    return module.generate


def build_signals(spec: StrategySpec, prices: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Run the strategy's `generate` and hold it to the signal contract."""
    signals = load_signal_function(spec.signal_path)(prices, spec.params)
    if not isinstance(signals, pd.DataFrame):
        raise TypeError("generate() must return a DataFrame, got %s" % type(signals).__name__)
    missing = [symbol for symbol in spec.universe if symbol not in signals.columns]
    if missing:
        raise ValueError("signal frame is missing universe columns: %s" % ", ".join(missing))
    signals = signals[spec.universe].astype(float)
    if bool(signals.isna().all(axis=None)):
        raise ValueError("signal frame is entirely NaN - start from pd.DataFrame(0.0, ...) and fill it in")
    if spec.long_only and bool((signals < -1e-9).any(axis=None)):
        raise ValueError("%s is long_only but the signal goes short (min %.3f)" % (spec.id, float(signals.min(axis=None))))
    if not np.isfinite(signals.fillna(0.0).to_numpy()).all():
        raise ValueError("signal frame contains inf - divide by zero somewhere?")
    gross = signals.abs().sum(axis=1)
    if bool((gross > spec.max_gross_exposure + 1e-9).any()):
        raise ValueError(
            "gross exposure %.2f exceeds max_gross_exposure %.2f - size your weights, do not stack them"
            % (float(gross.max()), spec.max_gross_exposure)
        )
    if spec.rebalance != "daily":
        signals = apply_rebalance(signals, spec.rebalance)
    return signals.fillna(0.0)


def apply_rebalance(signals: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Only let the target change on the last bar of each week/month; hold in between."""
    freq = {"weekly": "W", "monthly": "M"}.get(rule)
    if freq is None:
        raise ValueError("unknown rebalance rule %r" % rule)
    periods = signals.index.to_period(freq)
    is_decision_bar = ~pd.Series(periods, index=signals.index).duplicated(keep="last")
    return signals.where(is_decision_bar).ffill().fillna(0.0)


# --------------------------------------------------------------------------- #
# 4. RESULT
# --------------------------------------------------------------------------- #
@dataclass
class BacktestResult:
    """The only shape anything downstream needs to understand."""

    name: str
    equity: pd.Series
    returns: pd.Series
    positions: pd.DataFrame
    trades: pd.DataFrame
    prices: Optional[pd.DataFrame]
    meta: Dict[str, Any]

    @property
    def metrics(self) -> Dict[str, float]:
        return metrics_mod.summary(self.equity, trades=self.trades)

    @property
    def turnover(self) -> float:
        """Average per-bar gross turnover - the number that predicts cost deaths."""
        return float(self.meta.get("turnover_per_bar", self.meta.get("turnover_annual", float("nan"))))

    def metrics_with(self, **extra: float) -> Dict[str, float]:
        out = dict(self.metrics)
        out.update(extra)
        return out

    def state_at(self, timestamp) -> Dict[str, Any]:
        """Positions and equity as of a bar. This is the bridge used in Weeks 11-12
        to ask 'what would the backtest have been holding on this date?'"""
        ts = pd.Timestamp(timestamp)
        if ts not in self.positions.index:
            prior = self.positions.index[self.positions.index <= ts]
            if len(prior) == 0:
                raise KeyError("no bars at or before %s" % ts)
            ts = prior[-1]
        return {
            "timestamp": str(ts.date()),
            "equity": float(self.equity.loc[ts]),
            "positions": {k: float(v) for k, v in self.positions.loc[ts].items() if abs(float(v)) > 1e-12},
        }

    def save(self, directory: Optional[str] = None, results_dir: str = RESULTS_DIR) -> str:
        out_dir = directory or os.path.join(results_dir, self.name)
        os.makedirs(out_dir, exist_ok=True)
        equity = self.equity.rename("equity")
        equity.index.name = "date"
        equity.to_frame().to_csv(os.path.join(out_dir, "equity.csv"))
        positions = self.positions.copy()
        positions.index.name = "date"
        positions.to_csv(os.path.join(out_dir, "positions.csv"))
        self.trades.to_csv(os.path.join(out_dir, "trades.csv"), index=False)
        with open(os.path.join(out_dir, "metrics.json"), "w", encoding="utf-8") as fh:
            json.dump({k: float(v) for k, v in self.metrics.items()}, fh, indent=2, sort_keys=True)
        with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as fh:
            json.dump(self.meta, fh, indent=2, sort_keys=True, default=str)
        return out_dir

    @classmethod
    def load(cls, name_or_path: str, results_dir: str = RESULTS_DIR) -> "BacktestResult":
        directory = name_or_path if os.path.isdir(name_or_path) else os.path.join(results_dir, name_or_path)
        equity = pd.read_csv(os.path.join(directory, "equity.csv"), parse_dates=["date"]).set_index("date")["equity"]
        positions = pd.read_csv(os.path.join(directory, "positions.csv"), parse_dates=["date"]).set_index("date")
        trades_path = os.path.join(directory, "trades.csv")
        trades = pd.read_csv(trades_path) if os.path.exists(trades_path) and os.path.getsize(trades_path) > 0 else pd.DataFrame()
        for column in ("entry_time", "exit_time"):
            if column in trades.columns:
                trades[column] = pd.to_datetime(trades[column])
        meta_path = os.path.join(directory, "meta.json")
        meta = json.load(open(meta_path, "r", encoding="utf-8")) if os.path.exists(meta_path) else {}
        return cls(
            name=str(meta.get("name", os.path.basename(directory))),
            equity=equity,
            returns=metrics_mod.to_returns(equity),
            positions=positions,
            trades=trades,
            prices=None,
            meta=meta,
        )


# --------------------------------------------------------------------------- #
# the backtester itself (deliberately plain)
# --------------------------------------------------------------------------- #
def run_backtest(
    spec: StrategySpec,
    name: Optional[str] = None,
    prices: Optional[Dict[str, pd.DataFrame]] = None,
    signals: Optional[pd.DataFrame] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    initial_capital: float = INITIAL_CAPITAL,
    fee_bps: float = 0.0,
    slippage_bps: float = 0.0,
    execution: str = "next_open",
    data_dir: str = DATA_DIR,
    signal_shift: int = 1,
) -> BacktestResult:
    """Spec -> signals -> next-bar execution -> equity, positions, trades, metadata.

    `signal_shift` exists so you can run the Week 3 look-ahead experiment:
    signal_shift=0 fills the decision on its own bar, which is cheating, and the
    improvement you see is the size of your look-ahead bug. Never report it.
    """
    if prices is None:
        prices = load_universe(spec.universe, start, end, data_dir)
    if signals is None:
        signals = build_signals(spec, prices)

    closes = close_frame({s: prices[s] for s in spec.universe if s in prices})
    if start:
        closes = closes[closes.index >= pd.Timestamp(start)]
    if end:
        closes = closes[closes.index <= pd.Timestamp(end)]
    if len(closes) < 2:
        raise ValueError("not enough bars to backtest (%d)" % len(closes))
    signals = signals.reindex(closes.index).ffill().fillna(0.0)

    target = signals.shift(signal_shift).fillna(0.0) if signal_shift > 0 else signals.fillna(0.0)
    gross_exposure = target.abs().sum(axis=1)
    scale = pd.Series(1.0, index=target.index)
    over = gross_exposure > spec.max_gross_exposure
    scale[over] = spec.max_gross_exposure / gross_exposure[over]
    target = target.mul(scale, axis=0)

    closes_flat = closes.ffill()
    c2c = closes_flat.pct_change().fillna(0.0)
    if execution == "next_close":
        strategy_returns = target * c2c
    elif execution == "next_open":
        opens = pd.DataFrame(
            {s: prices[s]["open"] for s in closes.columns if s in prices}
        ).reindex(closes.index).ffill()
        opens = opens.where(opens > 0).ffill().bfill()
        overnight = (opens / closes_flat.shift(1) - 1.0).fillna(0.0)
        intraday = (closes_flat / opens - 1.0).fillna(0.0)
        # the position held INTO bar t is target[t-1] (filled at bar t-1's open);
        # the position established AT bar t's open is target[t]. Note the two
        # different lags: this asymmetry is the gap you pay when chasing opens.
        strategy_returns = target.shift(1).fillna(0.0) * overnight + target * intraday
    else:
        raise ValueError("execution must be 'next_open' or 'next_close'")

    turnover = target.diff().abs().sum(axis=1)
    turnover.iloc[0] = target.iloc[0].abs().sum()
    cost_rate = (fee_bps + slippage_bps) / 10_000.0
    gross_returns = strategy_returns.sum(axis=1)
    cost_drag = turnover * cost_rate
    net_returns = gross_returns - cost_drag
    equity = initial_capital * (1.0 + net_returns).cumprod()
    equity.iloc[0] = initial_capital

    trades = extract_trades(target, c2c, equity, cost_rate)
    meta = {
        "name": name or spec.id,
        "strategy_id": spec.id,
        "strategy_name": spec.name,
        "params": spec.params,
        "universe": spec.universe,
        "spec_fingerprint": spec.fingerprint(),
        "data_fingerprint": data_fingerprint(list(closes.columns), data_dir),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "engine": "kit.spine (reference)",
        "execution": execution,
        "signal_shift": signal_shift,
        "fee_bps": fee_bps,
        "slippage_bps": slippage_bps,
        "initial_capital": initial_capital,
        "bars": int(len(closes)),
        "first_bar": str(closes.index[0].date()),
        "last_bar": str(closes.index[-1].date()),
        "turnover_per_bar": float(turnover.mean()),
        "turnover_annual": float(turnover.mean() * metrics_mod.periods_per_year(closes.index)),
        "total_cost_drag": float(cost_drag.sum()),
    }
    equity.index.name = "date"
    return BacktestResult(
        name=str(meta["name"]),
        equity=equity.rename("equity"),
        returns=net_returns.rename("returns"),
        positions=target,
        trades=trades,
        prices=closes_flat,
        meta=meta,
    )


def extract_trades(target: pd.DataFrame, symbol_returns: pd.DataFrame, equity: pd.Series, cost_rate: float = 0.0) -> pd.DataFrame:
    """Weight path -> round-trip trades. A flip closes one trade and opens another."""
    rows: List[Dict[str, Any]] = []
    for symbol in target.columns:
        weights = target[symbol].fillna(0.0)
        rets = symbol_returns[symbol].fillna(0.0) if symbol in symbol_returns.columns else pd.Series(0.0, index=target.index)
        state = 0.0
        entry_idx = 0
        peak_weight = 0.0
        for i, (timestamp, weight) in enumerate(weights.items()):
            new_sign = float(np.sign(weight)) if abs(weight) > 1e-12 else 0.0
            if new_sign != state:
                if state != 0.0 and i > entry_idx:
                    rows.append(_trade_row(symbol, weights, rets, equity, entry_idx, i, state, peak_weight, cost_rate))
                state = new_sign
                entry_idx = i
                peak_weight = abs(weight)
            elif state != 0.0 and abs(weight) > peak_weight:
                peak_weight = abs(weight)
        if state != 0.0 and len(weights) - 1 > entry_idx:
            rows.append(_trade_row(symbol, weights, rets, equity, entry_idx, len(weights) - 1, state, peak_weight, cost_rate))
    if not rows:
        return pd.DataFrame(columns=["symbol", "side", "entry_time", "exit_time", "bars_held", "avg_weight", "pnl", "return"])
    return pd.DataFrame(rows).sort_values(["entry_time", "symbol"]).reset_index(drop=True)


def _trade_row(symbol, weights, rets, equity, entry_idx, exit_idx, side, avg_weight, cost_rate) -> Dict[str, Any]:
    window = rets.iloc[entry_idx + 1: exit_idx + 1]
    gross = float((1.0 + window).prod() - 1.0)
    pnl_pct = gross if side > 0 else (-gross if gross > -1 else -0.999)  # short: mirrored, floored at -100%
    notional = avg_weight * float(equity.iloc[max(entry_idx, 0)])
    cost = notional * 2.0 * avg_weight * cost_rate  # in and out, on the traded notional
    return {
        "symbol": symbol,
        "side": "long" if side > 0 else "short",
        "entry_time": weights.index[entry_idx],
        "exit_time": weights.index[exit_idx],
        "bars_held": int(exit_idx - entry_idx),
        "avg_weight": float(avg_weight),
        "return": float(pnl_pct),
        "pnl": float(notional * pnl_pct - cost),
        "cost": float(cost),
    }


# --------------------------------------------------------------------------- #
# convenience runners
# --------------------------------------------------------------------------- #
def run_spec(strategy_id: str, name: Optional[str] = None, save: bool = True, **kwargs) -> BacktestResult:
    spec = load_spec(strategy_id)
    result = run_backtest(spec, name=name or strategy_id, **kwargs)
    if save:
        result.save()
    return result


def compare(left: str, right: str, results_dir: str = RESULTS_DIR) -> str:
    """Side-by-side metric table for two saved backtests. This is how you argue with yourself."""
    a, b = BacktestResult.load(left, results_dir), BacktestResult.load(right, results_dir)
    keys = sorted(set(a.metrics) | set(b.metrics))
    lines = ["| metric | %s | %s | delta |" % (a.name, b.name), "| --- | --- | --- | --- |"]
    for key in keys:
        va, vb = a.metrics.get(key, float("nan")), b.metrics.get(key, float("nan"))
        lines.append(
            "| `%s` | %s | %s | %s |"
            % (key, metrics_mod.format_metric(key, va), metrics_mod.format_metric(key, vb), metrics_mod.format_metric(key, vb - va))
        )
    return "\n".join(lines)


def cost_breakeven(strategy_id: str, name: Optional[str] = None, bps_grid: Optional[Sequence[float]] = None, **kwargs) -> pd.DataFrame:
    """Where does this strategy die? Returns net Sharpe/CAGR per round-trip cost level."""
    bps_grid = list(bps_grid or [0.0, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 30.0])
    spec = load_spec(strategy_id)
    rows = []
    for bps in bps_grid:
        result = run_backtest(spec, name="%s_%gbps" % (name or strategy_id, bps), fee_bps=bps, slippage_bps=0.0, **kwargs)
        rows.append(
            {
                "fee_bps_roundtrip": bps,
                "cagr": result.metrics["cagr"],
                "sharpe": result.metrics["sharpe"],
                "max_drawdown": result.metrics["max_drawdown"],
                "total_return": result.metrics["total_return"],
            }
        )
    return pd.DataFrame(rows)


def _main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PyTrades backtest spine")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list strategy specs in config/")

    p_run = sub.add_parser("run", help="run a strategy spec")
    p_run.add_argument("strategy_id")
    p_run.add_argument("--name", default=None)
    p_run.add_argument("--start", default=None)
    p_run.add_argument("--end", default=None)
    p_run.add_argument("--fee-bps", type=float, default=0.0)
    p_run.add_argument("--slippage-bps", type=float, default=0.0)
    p_run.add_argument("--print-trades", action="store_true")

    p_brk = sub.add_parser("breakeven", help="cost grid where a strategy dies")
    p_brk.add_argument("strategy_id")
    p_brk.add_argument("--start", default=None)
    p_brk.add_argument("--end", default=None)

    p_cmp = sub.add_parser("compare", help="compare two saved backtests")
    p_cmp.add_argument("left")
    p_cmp.add_argument("right")

    args = parser.parse_args(argv)

    if args.command == "list":
        specs = list_specs()
        if not specs:
            print("no specs in config/ - copy the schema from shared/templates/strategy-config-schema.md")
            return 0
        for spec in specs:
            print("%-22s %-40s %s" % (spec.id, spec.name, ",".join(spec.universe[:6]) + ("..." if len(spec.universe) > 6 else "")))
        return 0

    if args.command == "run":
        result = run_spec(
            args.strategy_id,
            name=args.name,
            start=args.start,
            end=args.end,
            fee_bps=args.fee_bps,
            slippage_bps=args.slippage_bps,
        )
        print("backtest '%s' -> reports/backtests/%s/" % (result.name, result.name))
        print(metrics_mod.tearsheet(result.metrics, title=result.name))
        if args.print_trades and len(result.trades):
            print(result.trades.to_string(index=False))
        return 0

    if args.command == "breakeven":
        table = cost_breakeven(args.strategy_id, start=args.start, end=args.end)
        print(table.to_string(index=False, float_format=lambda v: "%.4f" % v))
        return 0

    if args.command == "compare":
        print(compare(args.left, args.right))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(_main())
