#!/usr/bin/env python3
"""tools/doctor.py - is this machine ready to trade (on paper) yet?

Run: make doctor

Checks the interpreter, dependencies, repo skeleton, data, and your position in
the 13-week calendar. Creates course.json on first run so the gate runner knows
which week you are in.
"""

from __future__ import annotations

import glob
import importlib
import json
import os
import sys
from datetime import date, datetime

MIN_PYTHON = (3, 10)
REQUIRED = ["pandas", "numpy", "pytest"]
OPTIONAL = {1: ["matplotlib"], 6: ["scipy"], 8: ["statsmodels"], 11: ["alpaca-py", "ccxt"]}
REQUIRED_DIRS = ["config", "data", "kit", "strategies", "reports", "journal", "tools", "tests"]


def line(ok: bool, label: str, detail: str = "") -> None:
    mark = "\033[32mok\033[0m" if ok else "\033[33mwarn\033[0m"
    print("  %s  %-28s %s" % (mark, label, detail))


def main() -> int:
    problems: list[str] = []
    print("PyTrades doctor")
    print("-" * 60)

    version = sys.version_info
    line(version >= MIN_PYTHON, "python >= %d.%d" % MIN_PYTHON, "found %d.%d.%d" % (version.major, version.minor, version.micro))
    if version < MIN_PYTHON:
        problems.append("upgrade Python to 3.10+")

    for name in REQUIRED:
        try:
            module = importlib.import_module(name)
            line(True, name, getattr(module, "__version__", "installed"))
        except ImportError:
            line(False, name, "MISSING - pip install -r requirements.txt")
            problems.append("install %s" % name)

    try:
        import pandas as pd  # noqa: F401

        for name in OPTIONAL[1]:
            try:
                importlib.import_module(name)
                line(True, name, "optional, installed")
            except ImportError:
                line(False, name, "optional - needed for chart-heavy reports")
    except ImportError:
        pass

    for directory in REQUIRED_DIRS:
        exists = os.path.isdir(directory)
        line(exists, directory + "/", "" if exists else "missing (make scaffold)")
        if not exists:
            problems.append("run: make scaffold")

    data_files = sorted(glob.glob("data/*.csv"))
    line(len(data_files) > 0, "cached data", "%d CSV file(s)" % len(data_files))
    if not data_files:
        print("      fetch your first series:  make data SYMBOLS=\"SPY QQQ\" START=2010-01-01")
    else:
        print("      %s" % ", ".join(os.path.basename(p)[:-4] for p in data_files[:12]))

    line(os.path.exists("gates.json"), "gates.json", "gate runner data")
    if not os.path.exists("gates.json"):
        problems.append("gates.json missing - copy it from the course package (shared/repo-scaffold/gates.json)")

    started = None
    if os.path.exists("course.json"):
        with open("course.json", "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        started = payload.get("started_at")
        line(True, "course.json", "started %s" % started)
    else:
        started = date.today().isoformat()
        with open("course.json", "w", encoding="utf-8") as fh:
            json.dump({"started_at": started, "student": "you", "note": "created by tools/doctor.py"}, fh, indent=2)
        line(True, "course.json", "created, course starts today (%s)" % started)

    if started:
        day = (date.today() - datetime.fromisoformat(str(started)[:10]).date()).days + 1
        week = max(1, min(13, (day - 1) // 7 + 1))
        print("  --   %-28s day %d, week %d of 13" % ("calendar", day, week))

    print("-" * 60)
    if problems:
        print("Fix these first, then re-run: make doctor")
        for problem in problems:
            print("  - %s" % problem)
        return 1
    print("Everything green. Start with Week 1: fetch data, build an equity curve, measure it.")
    print("Next:  make data SYMBOLS=\"SPY QQQ IWM TLT GLD\" START=2005-01-01")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
