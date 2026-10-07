#!/usr/bin/env python3
"""tools/validate_all.py - every cached series, checked, in one table.

Run: make validate

Anything that fails here must be fixed (re-fetch, replace, or document) before it
can appear in a backtest. A verdict built on an unvalidated CSV is a guess with
a chart attached.
"""

from __future__ import annotations

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kit import data_fetcher as df  # noqa: E402


def main() -> int:
    paths = sorted(glob.glob("data/*.csv"))
    if not paths:
        print("no CSVs in data/ - run: make data SYMBOLS=\"SPY QQQ\" START=2010-01-01")
        return 1

    rows = []
    failures = 0
    for path in paths:
        symbol = os.path.basename(path)[:-4]
        meta = df.read_meta(symbol)
        try:
            frame = df.load(symbol)
        except Exception as exc:  # noqa: BLE001
            rows.append({"symbol": symbol, "rows": 0, "first": "-", "last": "-", "issues": 1, "warnings": 0, "verdict": "FAIL", "source": "unreadable: %s" % exc})
            failures += 1
            continue
        report = df.validate(frame, symbol)
        failures += 0 if report.ok else 1
        rows.append(
            {
                "symbol": symbol,
                "rows": report.rows,
                "first": report.first,
                "last": report.last,
                "issues": len(report.issues),
                "warnings": len(report.warnings),
                "verdict": "ok" if report.ok else "FAIL",
                "source": meta.get("provider", "unknown") + (" (SYNTHETIC)" if report.synthetic else ""),
            }
        )

    headers = ["symbol", "rows", "first", "last", "issues", "warnings", "verdict", "source"]
    widths = {h: max(len(h), max(len(str(r[h])) for r in rows)) for h in headers}
    print(" ".join(h.ljust(widths[h]) for h in headers))
    print(" ".join("-" * widths[h] for h in headers))
    for row in rows:
        print(" ".join(str(row[h]).ljust(widths[h]) for h in headers))

    print()
    for path in paths:
        symbol = os.path.basename(path)[:-4]
        try:
            report = df.validate(df.load(symbol), symbol)
        except Exception:  # noqa: BLE001
            continue
        if report.issues or report.warnings:
            print(report)
            print()
        if report.synthetic:
            print("NOTE %s is synthetic data. It can smoke-test your pipeline; it cannot support a verdict." % symbol)

    print("%d file(s), %d with fatal issues" % (len(paths), failures))
    if failures:
        print("Fix the failures, or document them in reports/data-validation.md and exclude those symbols.")
        return 1
    print("All cached data is clean. Write the coverage table into reports/data-validation.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
