#!/usr/bin/env python3
"""tools/check_gate.py - the gate runner. Ship, or don't advance.

Reads gates.json (generated from the course registry) and checks each item
against what is actually in your repo. Mechanical checks are verified for you;
"manual" checks are yours to confirm - the runner will not let you advance until
you have confirmed them by name, and confirming a lie is a lie you tell yourself.

    make gate WEEK=1
    python tools/check_gate.py --week 1
    python tools/check_gate.py --all
    python tools/check_gate.py --week 1 --confirm G1.7
    python tools/check_gate.py --week 1 --explain G1.3
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

GATES_PATH = "gates.json"
CONFIRM_PATH = "reports/gates/confirmed.json"
COURSE_PATH = "course.json"

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_json(path: str, default: Any = None) -> Any:
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: str, payload: Any) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)


def course_started() -> Optional[date]:
    payload = load_json(COURSE_PATH, {}) or {}
    raw = payload.get("started_at")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw)[:10]).date()
    except ValueError:
        return None


def week_window(week: int) -> Optional[Tuple[date, date]]:
    start = course_started()
    if start is None:
        return None
    first = start + timedelta(days=7 * (week - 1))
    return first, first + timedelta(days=6)


# --------------------------------------------------------------------------- #
# check implementations
# --------------------------------------------------------------------------- #
def check_file_exists(check: Dict[str, Any]) -> Tuple[bool, str]:
    path = check["path"]
    return os.path.exists(path), "%s %s" % ("found" if os.path.exists(path) else "missing:", path)


def check_files_min(check: Dict[str, Any]) -> Tuple[bool, str]:
    matches = [p for p in glob.glob(check["glob"], recursive=True) if os.path.isfile(p)]
    needed = int(check.get("min", 1))
    return len(matches) >= needed, "%d/%d files match %s" % (len(matches), needed, check["glob"])


def check_file_contains_section(check: Dict[str, Any]) -> Tuple[bool, str]:
    path = check["path"]
    if not os.path.exists(path):
        return False, "missing: %s" % path
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    marker = check.get("section", "## ")
    count = len(re.findall(r"^%s.*$" % re.escape(marker.strip()), text, flags=re.MULTILINE)) if marker.strip() else 0
    needed = int(check.get("min_sections", 1))
    return count >= needed, "%d/%d '%s' sections in %s" % (count, needed, marker.strip(), path)


def check_pattern_in_file(check: Dict[str, Any]) -> Tuple[bool, str]:
    path = check["path"]
    if not os.path.exists(path):
        return False, "missing: %s" % path
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    hits = len(re.findall(check["pattern"], text, flags=re.IGNORECASE))
    needed = int(check.get("min_matches", 1))
    return hits >= needed, "%d/%d matches for /%s/ in %s" % (hits, needed, check["pattern"], path)


def check_csv_rows_min(check: Dict[str, Any]) -> Tuple[bool, str]:
    path = check["path"]
    if not os.path.exists(path):
        return False, "missing: %s" % path
    with open(path, "r", encoding="utf-8") as fh:
        rows = max(sum(1 for _ in fh) - 1, 0)  # minus header
    needed = int(check["min"])
    return rows >= needed, "%d/%d data rows in %s" % (rows, needed, path)


def check_journal_min(check: Dict[str, Any]) -> Tuple[bool, str]:
    entries = sorted(glob.glob("journal/*.md"))
    dated = [p for p in entries if re.search(r"\d{4}-\d{2}-\d{2}\.md$", os.path.basename(p))]
    week = int(check.get("week", 0))
    if week:
        window = week_window(week)
        if window is None:
            return len(dated) >= int(check["min"]), "%d dated entries (set started_at in course.json for week windows)" % len(dated)
        first, last = window
        in_week = [p for p in dated if first <= date.fromisoformat(os.path.basename(p)[:10]) <= last]
        return len(in_week) >= int(check["min"]), "%d/%d journal entries between %s and %s" % (
            len(in_week),
            int(check["min"]),
            first,
            last,
        )
    return len(dated) >= int(check["min"]), "%d/%d journal entries written" % (len(dated), int(check["min"]))


def check_command(check: Dict[str, Any]) -> Tuple[bool, str]:
    cmd = check["cmd"]
    try:
        completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=check.get("timeout", 900))
    except subprocess.TimeoutExpired:
        return False, "timed out: %s" % cmd
    expected = int(check.get("expect_exit", 0))
    tail = (completed.stdout.strip().splitlines() or [""])[-1][:120]
    return completed.returncode == expected, "`%s` exited %d (want %d) %s" % (cmd, completed.returncode, expected, tail)


def check_retro(check: Dict[str, Any]) -> Tuple[bool, str]:
    phase = str(check.get("phase", "")).lower()
    candidates = ["reports/retro-%s.md" % phase, "reports/retro_%s.md" % phase, "reports/retro-%s.md" % phase.replace("p", "phase-")]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            answered = sum(1 for q in ("killed the most", "biggest difference", "fooling myself") if q in text.lower())
            if answered >= 2:
                return True, "retro found at %s (%d/3 questions answered)" % (path, answered)
            return False, "%s exists but only %d/3 retro questions are answered" % (path, answered)
    return False, "missing: reports/retro-%s.md (template: shared/retro-template.md)" % phase


def check_manual(check: Dict[str, Any], confirmed: Dict[str, bool]) -> Tuple[bool, str]:
    if confirmed.get(check["id"]):
        return True, "you confirmed this on %s" % confirmed.get(check["id"])
    return False, "NOT CONFIRMED - %s" % check["desc"]


CHECKERS = {
    "file_exists": check_file_exists,
    "files_min": check_files_min,
    "file_contains_section": check_file_contains_section,
    "pattern_in_file": check_pattern_in_file,
    "csv_rows_min": check_csv_rows_min,
    "journal_min": check_journal_min,
    "command": check_command,
    "retro": check_retro,
}


# --------------------------------------------------------------------------- #
# gate evaluation
# --------------------------------------------------------------------------- #
def evaluate_week(week: int, gates: Dict[str, Any], confirmed: Dict[str, str], quiet: bool = False) -> Tuple[bool, List[str]]:
    entry = gates["weeks"].get(str(week))
    if entry is None:
        return False, ["week %d is not in gates.json" % week]
    results: List[str] = []
    ok = True
    manual_pending: List[Dict[str, Any]] = []
    for check in entry["checks"]:
        kind = check["type"]
        if kind == "manual":
            passed, detail = check_manual(check, confirmed)
            manual_pending.append(check)
        elif kind in CHECKERS:
            passed, detail = CHECKERS[kind](check)
        else:
            passed, detail = False, "unknown check type %r" % kind
        ok = ok and passed
        status = "%sPASS%s" % (GREEN, RESET) if passed else "%sFAIL%s" % (RED, RESET)
        if kind == "manual" and not passed:
            status = "%sTODO%s" % (YELLOW, RESET)
        line = "  %s %-6s %s" % (status, check["id"], detail)
        if not quiet or not passed:
            print(line)
    if not ok and manual_pending:
        pending_ids = [c["id"] for c in manual_pending if not confirmed.get(c["id"])]
        if pending_ids:
            print("  %sconfirm with:%s python tools/check_gate.py --week %d %s" % (YELLOW, RESET, week, " ".join("--confirm %s" % i for i in pending_ids)))
    return ok, results


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--week", type=int, default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--confirm", action="append", default=[], help="confirm a manual check id, e.g. --confirm G1.7")
    parser.add_argument("--explain", default=None, help="show the full text of one check id")
    parser.add_argument("--engine", default="kit.spine", help="engine module for command checks")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="check that the runner and gates.json are healthy (used by gate G1.6)",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    if not os.path.exists(GATES_PATH):
        print("%s not found. Run this from your repo root (the folder with Makefile)." % GATES_PATH, file=sys.stderr)
        return 2
    gates = load_json(GATES_PATH, {})
    confirmed: Dict[str, str] = load_json(CONFIRM_PATH, {}) or {}
    os.environ["PYTRADES_ENGINE"] = args.engine

    if args.confirm:
        for check_id in args.confirm:
            unknown = all(check_id not in {c["id"] for c in entry["checks"]} for entry in gates["weeks"].values())
            if unknown:
                print("no such check id: %s" % check_id, file=sys.stderr)
                return 2
            confirmed[check_id] = date.today().isoformat()
        save_json(CONFIRM_PATH, confirmed)
        print("confirmed: %s" % ", ".join(args.confirm))

    if args.explain:
        for entry in gates["weeks"].values():
            for check in entry["checks"]:
                if check["id"] == args.explain:
                    print(json.dumps(check, indent=2))
                    print("\ncheckpoint for this week:\n  " + entry["checkpoint"])
                    return 0
        print("no such check id: %s" % args.explain, file=sys.stderr)
        return 2

    if args.list:
        for week_key in sorted(gates["weeks"], key=int):
            entry = gates["weeks"][week_key]
            print("week %-2s %-38s %d checks  %s" % (week_key, entry["title"], len(entry["checks"]), entry.get("milestone") or ""))
        return 0

    if args.all:
        print("=" * 74)
        print("GATE PROGRESS")
        print("=" * 74)
        frontier = None
        for week_key in sorted(gates["weeks"], key=int):
            week = int(week_key)
            entry = gates["weeks"][week_key]
            passed = True
            for check in entry["checks"]:
                kind = check["type"]
                if kind == "manual":
                    ok, _ = check_manual(check, confirmed)
                elif kind in CHECKERS:
                    ok, _ = CHECKERS[kind](check)
                else:
                    ok = False
                passed = passed and ok
            print("%s week %-2d %-40s %s" % (GREEN + "PASS" + RESET if passed else RED + "FAIL" + RESET, week, entry["title"], entry.get("milestone") or ""))
            if passed and frontier is None and week == max(int(k) for k in gates["weeks"]):
                frontier = week
        print("-" * 74)
        print("Gate 1..N must pass in order. Check the first FAIL and fix that before anything else.")
        return 0

    if args.week is None:
        parser.print_help()
        return 2

    entry = gates["weeks"].get(str(args.week))
    if entry is None:
        print("week %d is not a gate week" % args.week, file=sys.stderr)
        return 2
    print("=" * 74)
    print("WEEK %d GATE - %s" % (args.week, entry["title"]))
    print("=" * 74)
    print("checkpoint: %s" % entry["checkpoint"])
    print("ships: %s" % ", ".join(entry["deliverables"]) + ("   milestone: %s" % entry["milestone"] if entry.get("milestone") else ""))
    print()
    ok, _ = evaluate_week(args.week, gates, confirmed)
    print()
    print("graveyard prompt for this week:")
    print("  " + entry["graveyard_prompt"])
    print()
    if ok:
        print("%sGATE %d PASSED%s - advance. Journal the verdict, update the graveyard, log the concept." % (GREEN, args.week, RESET))
        return 0
    print("%sGATE %d NOT PASSED%s - do not advance. Fix the failures above first." % (RED, args.week, RESET))
    return 1


def _self_test() -> int:
    """Health check for the gate runner itself: `python tools/check_gate.py --week 1 --self-test`.

    Verifies the things a student's Week 1 gate depends on: gates.json parses and
    covers the whole course, every check has an id and a known type, and the
    runtime (course.json, today's date) is readable. Exit 0 = healthy, 2 = broken.
    """
    problems: List[str] = []
    if not os.path.exists(GATES_PATH):
        print("self-test: %s is missing" % GATES_PATH, file=sys.stderr)
        return 2
    try:
        with open(GATES_PATH, "r", encoding="utf-8") as handle:
            gates = json.load(handle)
    except (OSError, ValueError) as exc:
        print("self-test: gates.json is unreadable: %s" % exc, file=sys.stderr)
        return 2

    weeks = gates.get("weeks") or {}
    if len(weeks) != 13:
        problems.append("expected 13 weeks in gates.json, found %d" % len(weeks))
    known_types = {
        "file_exists", "files_min", "file_contains_section", "pattern_in_file",
        "journal_min", "command", "csv_rows_min", "retro", "manual",
    }
    seen_ids = set()
    for key, entry in weeks.items():
        checks = entry.get("checks") or []
        if not checks:
            problems.append("week %s has no checks" % key)
        for check in checks:
            check_id = check.get("id")
            if not check_id:
                problems.append("week %s has a check without an id" % key)
            elif check_id in seen_ids:
                problems.append("duplicate check id %s" % check_id)
            else:
                seen_ids.add(check_id)
            if check.get("type") not in known_types:
                problems.append("%s has unknown type %r" % (check_id, check.get("type")))
    if os.path.exists(COURSE_PATH):
        try:
            with open(COURSE_PATH, "r", encoding="utf-8") as handle:
                json.load(handle)
        except (OSError, ValueError) as exc:
            problems.append("course.json is unreadable: %s" % exc)
    else:
        problems.append("course.json is missing (run: python tools/doctor.py)")

    if problems:
        print("self-test: FAILED")
        for problem in problems:
            print("  - %s" % problem)
        return 2
    print("self-test: ok (%d weeks, %d checks)" % (len(weeks), len(seen_ids)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
