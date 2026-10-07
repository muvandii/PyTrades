"""kit/data_fetcher.py - get real bars into `data/`, or refuse to lie to you.

Design rules
------------
1. Real providers by default (stooq, then yahoo). Both are free and keyless.
2. Everything is cached to `data/<SYMBOL>.csv` with a `data/<SYMBOL>.meta.json`
   sidecar (provider, fetched_at, rows, first/last bar, sha256). The sidecar is
   how you prove later that a verdict was computed on data you can re-fetch.
3. `validate()` is not optional. Prices that fail validation get a FAIL report,
   and `assert_clean()` raises so a broken CSV cannot reach a backtest.
4. Offline mode exists ONLY for smoke tests: synthetic series are clearly
   labelled and `assert_not_synthetic()` blocks them from any graded verdict.
   A synthetic backtest taught you about your code; it told you nothing about
   the market. Never write a verdict on one.

Usage
-----
    from kit.data_fetcher import fetch, fetch_many, load, validate, universe

    fetch("SPY", "2010-01-01", "2024-12-31")     # cache-aware, real data
    bars = fetch_many(universe("etf_core"), "2010-01-01", "2024-12-31")
    print(validate(bars["SPY"]))                  # human-readable report
    spy = load("SPY")                             # from cache, no network

CLI
---
    python -m kit.data_fetcher fetch SPY QQQ --start 2010-01-01
    python -m kit.data_fetcher validate SPY QQQ
    python -m kit.data_fetcher smoke            # offline synthetic self-test
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

USER_AGENT = "pytrades-bootcamp/1.0 (educational backtesting; contact: student)"
OHLCV = ["open", "high", "low", "close", "volume"]
DEFAULT_DATA_DIR = os.environ.get("PYTRADES_DATA", "data")
CACHE_MAX_AGE_DAYS = float(os.environ.get("PYTRADES_CACHE_DAYS", "3"))

UNIVERSES: Dict[str, List[str]] = {
    # Liquid ETFs: enough for trend, momentum and vol-targeting work.
    "etf_core": ["SPY", "QQQ", "IWM", "TLT", "IEF", "GLD", "EEM", "EFA", "DBC", "UUP"],
    # Cross-section of US large caps that have existed for the whole sample.
    "us_eq_20": [
        "AAPL", "MSFT", "JNJ", "JPM", "XOM", "PG", "KO", "WMT", "CVX", "HD",
        "MCD", "IBM", "CAT", "GE", "BA", "MMM", "PFE", "T", "VZ", "DIS",
    ],
    # Pairs-trading playground: same-sector pairs that people actually try.
    "pairs_candidates": ["KO", "PEP", "XOM", "CVX", "V", "MA", "GS", "MS", "HD", "LOW"],
}


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #
@dataclass
class ValidationReport:
    symbol: str
    rows: int = 0
    first: Optional[str] = None
    last: Optional[str] = None
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    synthetic: bool = False

    @property
    def ok(self) -> bool:
        return not self.issues

    def __str__(self) -> str:
        head = "%s: %d rows, %s -> %s" % (self.symbol, self.rows, self.first, self.last)
        if self.synthetic:
            head += "  [SYNTHETIC - not market data]"
        lines = [head]
        for issue in self.issues:
            lines.append("  FAIL  %s" % issue)
        for warn in self.warnings:
            lines.append("  warn  %s" % warn)
        if not self.issues and not self.warnings:
            lines.append("  ok    all checks passed")
        return "\n".join(lines)


def validate(df: pd.DataFrame, symbol: str = "?") -> ValidationReport:
    """Structural + sanity checks on an OHLCV frame. Issues are fatal, warnings are not."""
    report = ValidationReport(symbol=symbol)
    report.synthetic = bool(df.attrs.get("synthetic", False))
    if df is None or len(df) == 0:
        report.issues.append("empty frame")
        return report

    missing = [c for c in OHLCV[:4] if c not in df.columns]
    if missing:
        report.issues.append("missing required columns: %s" % ", ".join(missing))
        return report

    report.rows = len(df)
    report.first = str(df.index[0].date()) if isinstance(df.index, pd.DatetimeIndex) else str(df.index[0])
    report.last = str(df.index[-1].date()) if isinstance(df.index, pd.DatetimeIndex) else str(df.index[-1])

    if not isinstance(df.index, pd.DatetimeIndex):
        report.issues.append("index is not a DatetimeIndex")
        return report
    if not df.index.is_monotonic_increasing:
        report.issues.append("index is not sorted ascending")
    if df.index.has_duplicates:
        dupes = int(df.index.duplicated().sum())
        report.issues.append("%d duplicate timestamps" % dupes)
    if df.index.tz is not None:
        report.warnings.append("index is timezone-aware; backtests assume naive local dates")

    if df[["open", "high", "low", "close"]].isna().any().any():
        report.issues.append("NaNs in price columns")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        report.issues.append("non-positive prices")

    high_low_bad = int((df["high"] < df["low"]).sum())
    if high_low_bad:
        report.issues.append("%d bars where high < low" % high_low_bad)
    outside = int(((df["open"] > df["high"]) | (df["open"] < df["low"])).sum())
    if outside:
        report.warnings.append("%d bars where open sits outside [low, high] (dividend/split adjustments)" % outside)

    if "volume" in df.columns and (df["volume"] < 0).any():
        report.issues.append("negative volume")
    if "volume" in df.columns and len(df) > 20:
        zero_vol = float((df["volume"] == 0).mean())
        if zero_vol > 0.02:
            report.warnings.append("%.1f%% of bars have zero volume" % (zero_vol * 100))

    # calendar gaps: a silent hole is how survivorship and stale data sneak in
    if len(df) > 2:
        gaps = df.index.to_series().diff().dt.days.dropna()
        big = gaps[gaps > 10]
        if len(big):
            report.warnings.append("%d calendar gaps longer than 10 days (max %d)" % (len(big), int(big.max())))

    # stale runs: identical closes repeating look like a feed that stopped updating
    if len(df) > 5:
        repeats = (df["close"].diff() == 0).astype(int)
        run = best = 0
        for value in repeats.values:
            run = run + 1 if value else 0
            best = max(best, run)
        if best >= 5:
            report.warnings.append("close repeated for %d consecutive bars" % (best + 1))

    # return outliers: usually a data error, occasionally a split
    if len(df) > 20:
        rets = df["close"] / df["close"].shift(1) - 1
        extremes = rets[rets.abs() > 0.35]
        if len(extremes):
            report.warnings.append(
                "%d daily |return| > 35%% (first: %s, %.1f%%) - check for splits/dividends"
                % (len(extremes), extremes.index[0].date(), extremes.iloc[0] * 100)
            )
    return report


def assert_clean(df: pd.DataFrame, symbol: str = "?") -> pd.DataFrame:
    report = validate(df, symbol)
    if not report.ok:
        raise ValueError("data for %s failed validation:\n%s" % (symbol, report))
    if report.synthetic:
        raise ValueError(
            "data for %s is SYNTHETIC. Smoke tests only - no verdict may be written on it." % symbol
        )
    return df


def assert_not_synthetic(df: pd.DataFrame, symbol: str = "?") -> None:
    if df.attrs.get("synthetic", False) or "synthetic" in str(symbol).lower():
        raise ValueError("refusing to use synthetic data for %s in a graded result" % symbol)


# --------------------------------------------------------------------------- #
# providers
# --------------------------------------------------------------------------- #
def _http_get(url: str, timeout: int = 20) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed hosts
        return response.read()


def _stooq_url(symbol: str) -> str:
    return "https://stooq.com/q/d/l/?s=%s&i=d&d1=19700101" % symbol.lower()


def _fetch_stooq(symbol: str) -> pd.DataFrame:
    """Stooq: free daily OHLCV, US tickers as 'spy.us'. Good for ETFs and large caps."""
    text = _http_get(_stooq_url(symbol)).decode("utf-8", errors="replace")
    if "No data" in text or len(text.strip().splitlines()) < 2:
        raise ValueError("stooq returned no data for %s (try symbol like 'spy.us')" % symbol)
    frame = pd.read_csv(io.StringIO(text))
    frame.columns = [c.strip().lower() for c in frame.columns]
    if "date" not in frame.columns:
        raise ValueError("stooq response had no Date column for %s" % symbol)
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame = frame.dropna(subset=["date"]).set_index("date").sort_index()
    keep = [c for c in OHLCV if c in frame.columns]
    if len(keep) < 4:
        raise ValueError("stooq response missing OHLC columns for %s" % symbol)
    out = frame[keep].astype(float)
    for column in OHLCV:
        if column not in out.columns:
            out[column] = np.nan
    return out[OHLCV]


def _fetch_yahoo(symbol: str, start: Optional[str] = None, end: Optional[str] = None) -> pd.DataFrame:
    """Yahoo chart API: second opinion, and the only source that also gives adjusted closes."""
    period1 = int(pd.Timestamp(start or "1990-01-01").timestamp())
    period2 = int(pd.Timestamp(end or datetime.now(timezone.utc).date()).timestamp()) + 86400
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%s"
        "?period1=%d&period2=%d&interval=1d&events=div%%2Csplit" % (symbol.upper(), period1, period2)
    )
    payload = json.loads(_http_get(url).decode("utf-8", errors="replace"))
    result = (payload.get("chart") or {}).get("result")
    if not result:
        raise ValueError("yahoo returned no series for %s: %s" % (symbol, payload.get("chart", {}).get("error")))
    node = result[0]
    timestamps = node.get("timestamp") or []
    quote = ((node.get("indicators") or {}).get("quote") or [{}])[0]
    if not timestamps or not quote:
        raise ValueError("yahoo returned an empty series for %s" % symbol)
    frame = pd.DataFrame(
        {
            "open": quote.get("open"),
            "high": quote.get("high"),
            "low": quote.get("low"),
            "close": quote.get("close"),
            "volume": quote.get("volume"),
        },
        index=pd.to_datetime(pd.Series(timestamps).values, unit="s").normalize(),
    ).astype(float)
    adj = (((node.get("indicators") or {}).get("adjclose") or [{}])[0]).get("adjclose")
    if adj is not None:
        frame["adj_close"] = np.asarray(adj, dtype=float)
    frame["symbol"] = symbol.upper()
    frame = frame.dropna(subset=["close"]).sort_index()
    frame = frame[~frame.index.duplicated(keep="last")]
    for column in OHLCV:
        if column not in frame.columns:
            frame[column] = np.nan
    return frame[["open", "high", "low", "close", "volume"]]


PROVIDERS = {"stooq": _fetch_stooq, "yahoo": _fetch_yahoo}


# --------------------------------------------------------------------------- #
# synthetic (smoke tests only)
# --------------------------------------------------------------------------- #
def synthetic(symbol: str = "SYN", start: str = "2015-01-01", end: str = "2024-12-31", seed: int = 7) -> pd.DataFrame:
    """Deterministic fake bars for offline smoke tests.

    Contains a hidden trend signal and a vol-clustering regime, so your pipeline
    can be exercised end-to-end without network. It contains NO market truth.
    """
    index = pd.bdate_range(start, end)
    rng = np.random.default_rng(seed + (abs(hash(symbol)) % 10_000))
    n = len(index)
    vol = np.full(n, 0.010)
    for i in range(1, n):
        vol[i] = 0.94 * vol[i - 1] + 0.06 * 0.010
        if rng.random() < 0.01:
            vol[i] *= 3.0
    vol = np.clip(vol, 0.003, 0.055)
    drift = 0.00040 + 0.00030 * np.sin(np.arange(n) / 180.0)
    shocks = rng.standard_normal(n) * vol
    # a genuine, small, lag-1 trend component - enough for a cheap trend rule to work offline
    signal = 0.0009 * np.concatenate([[0.0], np.sign(shocks[:-1])])
    close = 100.0 * np.exp(np.cumsum(drift + signal + shocks))
    high = close * (1 + np.abs(rng.standard_normal(n)) * 0.004)
    low = close * (1 - np.abs(rng.standard_normal(n)) * 0.004)
    open_ = low + (high - low) * rng.random(n)
    frame = pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": rng.integers(1e6, 5e6, n).astype(float)},
        index=index,
    )
    frame.index.name = "date"
    frame.attrs["synthetic"] = True
    return frame


# --------------------------------------------------------------------------- #
# cache
# --------------------------------------------------------------------------- #
def _paths(symbol: str, data_dir: str) -> Tuple[str, str]:
    base = os.path.join(data_dir, symbol.upper())
    return base + ".csv", base + ".meta.json"


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cache_is_fresh(meta_path: str) -> bool:
    if not os.path.exists(meta_path):
        return False
    try:
        with open(meta_path, "r", encoding="utf-8") as fh:
            meta = json.load(fh)
        fetched = datetime.fromisoformat(meta["fetched_at"].replace("Z", "+00:00"))
    except Exception:
        return False
    age_days = (datetime.now(timezone.utc) - fetched).total_seconds() / 86400.0
    return age_days <= CACHE_MAX_AGE_DAYS


def read_meta(symbol: str, data_dir: str = DEFAULT_DATA_DIR) -> Dict[str, object]:
    _, meta_path = _paths(symbol, data_dir)
    if not os.path.exists(meta_path):
        return {}
    with open(meta_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def fetch(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    provider: str = "auto",
    data_dir: str = DEFAULT_DATA_DIR,
    refresh: bool = False,
    allow_synthetic: bool = False,
) -> pd.DataFrame:
    """Fetch (or load) one symbol. Writes CSV + meta.json into `data_dir`."""
    os.makedirs(data_dir, exist_ok=True)
    csv_path, meta_path = _paths(symbol, data_dir)

    if os.path.exists(csv_path) and not refresh and (_cache_is_fresh(meta_path) or provider == "cache"):
        return load(symbol, data_dir)

    if provider == "synthetic":
        if not allow_synthetic:
            raise ValueError(
                "synthetic data is for smoke tests only; pass allow_synthetic=True and never write a verdict on it"
            )
        frame = synthetic(symbol, start or "2015-01-01", end or "2024-12-31")
        return _persist(frame, symbol, "synthetic", data_dir)

    order = [provider] if provider in PROVIDERS else ["stooq", "yahoo"]
    errors: List[str] = []
    for name in order:
        try:
            frame = PROVIDERS[name](symbol) if name == "stooq" else PROVIDERS[name](symbol, start, end)
            if start is not None:
                frame = frame[frame.index >= pd.Timestamp(start)]
            if end is not None:
                frame = frame[frame.index <= pd.Timestamp(end)]
            if len(frame) == 0:
                raise ValueError("no rows in requested window")
            return _persist(frame, symbol, name, data_dir)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            errors.append("%s: network error %s" % (name, exc))
        except Exception as exc:  # noqa: BLE001 - provider errors are expected
            errors.append("%s: %s" % (name, exc))

    if os.path.exists(csv_path):
        print("fetch failed (%s); falling back to cached copy of %s" % ("; ".join(errors), symbol), file=sys.stderr)
        return load(symbol, data_dir)
    if allow_synthetic:
        print(
            "fetch failed (%s); generating SYNTHETIC data for %s because allow_synthetic=True.\n"
            "  Synthetic bars exercise code paths - they are not evidence about any market.\n"
            "  assert_not_synthetic() will refuse them in a graded backtest." % ("; ".join(errors), symbol),
            file=sys.stderr,
        )
        frame = synthetic(symbol, start or "2015-01-01", end or "2024-12-31")
        return _persist(frame, symbol, "synthetic", data_dir)
    raise RuntimeError(
        "could not fetch %s from %s.\n%s\n"
        "Options: check the ticker, verify network access, or use a CSV you already have:\n"
        "    df = kit.data_fetcher.load_csv('path/to/your.csv', symbol='%s')"
        % (symbol, " or ".join(order), "\n".join("  - " + e for e in errors), symbol)
    )


def _persist(frame: pd.DataFrame, symbol: str, provider: str, data_dir: str) -> pd.DataFrame:
    csv_path, meta_path = _paths(symbol, data_dir)
    out = frame.copy()
    out.index.name = "date"
    out.to_csv(csv_path, float_format="%.6f")
    meta = {
        "symbol": symbol.upper(),
        "provider": provider,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "rows": int(len(out)),
        "first": str(out.index[0].date()),
        "last": str(out.index[-1].date()),
        "synthetic": bool(out.attrs.get("synthetic", False)),
        "sha256": _sha256(csv_path),
    }
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    out.attrs["synthetic"] = meta["synthetic"]
    return out


def load(symbol: str, data_dir: str = DEFAULT_DATA_DIR) -> pd.DataFrame:
    """Load a cached CSV. This is what backtests should use: same bytes every run."""
    csv_path, _ = _paths(symbol, data_dir)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            "%s not in %s/ - run: python -m kit.data_fetcher fetch %s" % (csv_path, data_dir, symbol)
        )
    frame = pd.read_csv(csv_path, parse_dates=["date"]).set_index("date").sort_index()
    for column in OHLCV:
        if column not in frame.columns:
            frame[column] = float("nan")
    meta = read_meta(symbol, data_dir)
    frame.attrs["synthetic"] = bool(meta.get("synthetic", False))
    frame.attrs["meta"] = meta
    return frame[OHLCV].astype(float)


def load_csv(path: str, symbol: Optional[str] = None, date_column: str = "date") -> pd.DataFrame:
    """Load your own CSV. Column names are lower-cased; close is required."""
    frame = pd.read_csv(path)
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    if date_column not in frame.columns:
        for candidate in ("date", "datetime", "time", "timestamp"):
            if candidate in frame.columns:
                date_column = candidate
                break
        else:
            raise ValueError("%s has no date column (looked for date/datetime/time/timestamp)" % path)
    frame[date_column] = pd.to_datetime(frame[date_column])
    frame = frame.set_index(date_column).sort_index()
    for column in OHLCV:
        if column not in frame.columns:
            if column == "close" and "adj close" in frame.columns:
                frame["close"] = frame["adj close"]
            else:
                frame[column] = float("nan")
    return frame[OHLCV].astype(float)


def fetch_many(
    symbols: Iterable[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    provider: str = "auto",
    data_dir: str = DEFAULT_DATA_DIR,
    refresh: bool = False,
) -> Dict[str, pd.DataFrame]:
    """Fetch a universe. Failures are reported, not hidden - partial universes lie."""
    frames: Dict[str, pd.DataFrame] = {}
    failures: List[str] = []
    for symbol in symbols:
        try:
            frames[symbol] = fetch(symbol, start, end, provider, data_dir, refresh)
        except Exception as exc:  # noqa: BLE001
            failures.append("%s: %s" % (symbol, exc))
    if failures:
        print("failed to fetch %d symbol(s):\n  - %s" % (len(failures), "\n  - ".join(failures)), file=sys.stderr)
    return frames


def universe(name: str) -> List[str]:
    if name not in UNIVERSES:
        raise KeyError("unknown universe %r; known: %s" % (name, ", ".join(sorted(UNIVERSES))))
    return list(UNIVERSES[name])


def aligned_frame(frames: Dict[str, pd.DataFrame], field: str = "close", min_coverage: float = 0.95) -> pd.DataFrame:
    """Wide frame of one field across symbols, restricted to rows where enough symbols exist."""
    if not frames:
        raise ValueError("no frames to align")
    wide = pd.DataFrame({symbol: frame[field] for symbol, frame in frames.items()})
    coverage = wide.notna().mean(axis=1)
    return wide[coverage >= min_coverage].ffill().dropna(how="all")


def coverage_table(frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per symbol: rows, start, end, gaps, validation verdict. Print it in every report."""
    rows = []
    for symbol, frame in frames.items():
        report = validate(frame, symbol)
        rows.append(
            {
                "symbol": symbol,
                "rows": report.rows,
                "first": report.first,
                "last": report.last,
                "issues": len(report.issues),
                "warnings": len(report.warnings),
                "verdict": "ok" if report.ok else "FAIL",
            }
        )
    return pd.DataFrame(rows).sort_values("symbol").reset_index(drop=True)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PyTrades data fetcher")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="download bars into data/")
    p_fetch.add_argument("symbols", nargs="+")
    p_fetch.add_argument("--start", default=None)
    p_fetch.add_argument("--end", default=None)
    p_fetch.add_argument("--provider", default="auto", choices=["auto", "stooq", "yahoo", "synthetic"])
    p_fetch.add_argument("--universe", default=None, help="fetch a named universe instead of symbols")
    p_fetch.add_argument("--refresh", action="store_true")

    p_val = sub.add_parser("validate", help="validate cached symbols")
    p_val.add_argument("symbols", nargs="+")
    p_val.add_argument("--table", action="store_true")

    p_csv = sub.add_parser("ingest", help="bring your own CSV into data/")
    p_csv.add_argument("path")
    p_csv.add_argument("symbol")

    sub.add_parser("smoke", help="offline synthetic smoke test (no network, no truth)")
    args = parser.parse_args(argv)

    if args.command == "fetch":
        symbols = list(args.symbols) + (universe(args.universe) if args.universe else [])
        frames = fetch_many(symbols, args.start, args.end, args.provider, refresh=args.refresh)
        print(coverage_table(frames).to_string(index=False) if frames else "nothing fetched")
        return 0 if frames else 1

    if args.command == "validate":
        frames = {s: load(s) for s in args.symbols}
        if args.table:
            print(coverage_table(frames).to_string(index=False))
        else:
            for symbol, frame in frames.items():
                print(validate(frame, symbol))
        return 0 if all(validate(f, s).ok for s, f in frames.items()) else 1

    if args.command == "ingest":
        frame = load_csv(args.path)
        _persist(frame, args.symbol, "csv", DEFAULT_DATA_DIR)
        print(validate(frame, args.symbol))
        print("saved data/%s.csv" % args.symbol.upper())
        return 0

    if args.command == "smoke":
        frame = synthetic("SMOKE")
        report = validate(frame, "SMOKE")
        print(report)
        print("\nsynthetic smoke frame: %d bars, close %.2f -> %.2f" % (len(frame), frame["close"].iloc[0], frame["close"].iloc[-1]))
        print("Reminder: synthetic data may smoke-test your code, never your conclusions.")
        return 0 if report.ok else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(_main())
