#!/usr/bin/env python3
"""sync_gates.py - publish registry.json gates into the student repo's gate runner.

The course defines gates once, in registry.json. This tool flattens them into
`shared/repo-scaffold/gates.json`, which the student-side `tools/check_gate.py`
reads. One definition, two consumers, zero drift.

Usage
-----
    python bootcamp/tools/sync_gates.py            # write gates.json
    python bootcamp/tools/sync_gates.py --check    # exit 1 if gates.json is stale
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coursekit as ck  # noqa: E402

TARGET = "shared/repo-scaffold/gates.json"


def build(reg: Dict[str, Any]) -> Dict[str, Any]:
    weeks: Dict[str, Any] = {}
    for week in reg["weeks"]:
        gate = reg["gates"][str(week["n"])]
        checks = []
        for check in gate["checks"]:
            entry = {key: value for key, value in check.items() if key != "type"}
            entry["type"] = check["type"]
            entry["auto"] = check["type"] != "manual"
            checks.append(entry)
        weeks[str(week["n"])] = {
            "title": week["title"],
            "phase": week["phase"],
            "deliverables": week["deliverables"],
            "milestone": week["milestone"],
            "checkpoint": week["checkpoint"],
            "graveyard_prompt": week["graveyard_prompt"],
            "checks": checks,
        }
    return {
        "_comment": "Generated from bootcamp/registry.json by bootcamp/tools/sync_gates.py - do not edit by hand.",
        "course": reg["course"]["name"],
        "generated_from": "registry.json",
        "weeks": weeks,
    }


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    bc = ck.bootcamp_dir()
    reg = ck.load_registry(bc)
    path = os.path.join(bc, TARGET)
    payload = json.dumps(build(reg), indent=2, sort_keys=False) + "\n"

    current = ck.read_text(path) if os.path.exists(path) else ""
    if args.check:
        if current != payload:
            print("gates.json is STALE - run: python bootcamp/tools/sync_gates.py", file=sys.stderr)
            return 1
        print("gates.json is up to date (%d weeks, %d checks)" % (len(reg["weeks"]), sum(len(reg["gates"][k]["checks"]) for k in reg["gates"])))
        return 0

    if current == payload:
        print("gates.json already up to date")
        return 0
    ck.write_text(path, payload)
    print("wrote %s (%d weeks, %d checks)" % (TARGET, len(reg["weeks"]), sum(len(reg["gates"][k]["checks"]) for k in reg["gates"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
