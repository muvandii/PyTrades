#!/usr/bin/env python3
"""build_syllabus.py - regenerate the machine-owned tables inside syllabus.md.

The syllabus is the human index of the whole course. Every table in it that
describes weeks, concepts, deliverables, milestones, gates, grading or the
package tree is generated from registry.json (plus the real filesystem), so
the syllabus can never drift from the course.

Usage
-----
    python bootcamp/tools/build_syllabus.py            # rewrite syllabus.md
    python bootcamp/tools/build_syllabus.py --check    # exit 1 on drift
    python bootcamp/tools/build_syllabus.py --stdout   # print, do not write
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coursekit as ck  # noqa: E402

SYLLABUS = "syllabus.md"

TREE_SKIP = {"__pycache__", "generated", ".DS_Store", ".ipynb_checkpoints", ".gitkeep"}
TREE_SKIP_SUFFIX = (".pyc",)


# --------------------------------------------------------------------------- #
# block builders
# --------------------------------------------------------------------------- #
def block_weeks(reg: Dict[str, Any], bc: str) -> str:
    rows = []
    for w in reg["weeks"]:
        ms = w["milestone"] or "\u2014"
        phase_dir = next(p["dir"] for p in reg["phases"] if p["id"] == w["phase"])
        title = "[%s](phases/%s/week-%02d.md)" % (w["title"], phase_dir, w["n"])
        rows.append(
            [
                w["n"],
                w["phase"],
                title,
                ", ".join(w["deliverables"]),
                ", ".join(w["concepts"]) or "\u2014",
                ms,
                w["time_hours"],
            ]
        )
    return ck.md_table(
        ["Wk", "Phase", "Title", "Ships", "Concepts injected", "Milestone", "Hours"],
        rows,
        aligns=["--:", ":--", ":--", ":--", ":--", ":--", ":--"],
    )


def block_gates(reg: Dict[str, Any], bc: str) -> str:
    rows = []
    for w in reg["weeks"]:
        gate = reg["gates"][str(w["n"])]
        n_checks = len(gate["checks"])
        auto = sum(1 for c in gate["checks"] if c["type"] != "manual")
        rows.append(
            [
                w["n"],
                ck.truncate(w["checkpoint"], 130),
                "%d auto + %d manual" % (auto, n_checks - auto),
                w["milestone"] or "\u2014",
            ]
        )
    return ck.md_table(
        ["Wk", "Gate: you do not advance until", "Verified by", "Milestone"],
        rows,
        aligns=["--:", ":--", ":--", ":--"],
    )


def block_concepts(reg: Dict[str, Any], bc: str) -> str:
    by_id = {c["id"]: c for c in reg["concepts"]}
    rows = []
    for c in sorted(reg["concepts"], key=lambda x: (x["week"], x["id"])):
        rel_path = c["file"]
        link = "[%s](%s)" % (c["id"], rel_path)
        rows.append(
            [
                "T%d" % c["tier"],
                c["week"],
                link,
                c["name"],
                "[%s](%s)" % (c["deliverable"], _deliverable_link(reg, c["deliverable"])),
                ck.truncate(c["trigger"], 96),
            ]
        )
    return ck.md_table(
        ["Tier", "Wk", "ID", "Concept", "Demanded by", "Triggering failure"],
        rows,
        aligns=[":--", "--:", ":--", ":--", ":--", ":--"],
    )


def _deliverable_link(reg: Dict[str, Any], deliverable_id: str) -> str:
    d = ck.deliverable_by_id(reg, deliverable_id)
    if not d:
        return "registry.json"
    phase = next(p for p in reg["phases"] if p["id"] == d["phase"])
    return "phases/%s/deliverables/%s.md" % (phase["dir"], deliverable_id)


def block_deliverables(reg: Dict[str, Any], bc: str) -> str:
    rows = []
    for d in sorted(reg["deliverables"], key=lambda x: x["week"]):
        rows.append(
            [
                d["id"],
                d["week"],
                "[%s](%s)" % (d["title"], _deliverable_link(reg, d["id"])),
                d["milestone"],
                ck.truncate(d["teaches"], 90),
            ]
        )
    return ck.md_table(
        ["ID", "Wk", "Deliverable", "Milestone", "Teaches exactly one thing"],
        rows,
        aligns=[":--", "--:", ":--", ":--", ":--"],
    )


def block_milestones(reg: Dict[str, Any], bc: str) -> str:
    rows = []
    for m in reg["milestones"]:
        rows.append(
            [
                m["id"],
                m["week"],
                "[%s](%s)" % (m["name"], _milestone_link(reg, m)),
                ck.truncate(m["pass_condition"], 150),
            ]
        )
    return ck.md_table(
        ["ID", "Wk", "Milestone", "Pass condition (hard gate)"],
        rows,
        aligns=[":--", "--:", ":--", ":--"],
    )


def _milestone_link(reg: Dict[str, Any], m: Dict[str, Any]) -> str:
    week = ck.by_week(reg, m["week"])
    phase = next(p for p in reg["phases"] if p["id"] == week["phase"])
    return "phases/%s/milestones/%s-%s.md" % (
        phase["dir"],
        m["id"],
        m["name"].lower().replace(" & ", "-").replace(" ", "-"),
    )


def block_grading(reg: Dict[str, Any], bc: str) -> str:
    g = reg["grading"]
    rows = [[a["artifact"], "%d%%" % a["weight"], a["passing_bar"]] for a in g["artifacts"]]
    rows.append(["**Total**", "**%d%%**" % sum(a["weight"] for a in g["artifacts"]), "60% = pass, 80% = good, 90%+ = publication-worthy"])
    return ck.md_table(["Artifact", "Weight", "Passing bar"], rows, aligns=[":--", "--:", ":--"])


def block_annotations(reg: Dict[str, Any], bc: str) -> str:
    """Cross-reference every annotated block: which deliverable it evidences."""
    rows = []
    for path in sorted(ck.glob_files(bc, "**/*.md")):
        if ck.rel(bc, path).startswith("generated/"):
            continue
        text = ck.read_text(path)
        produces = ck.declared_ids(text, "produces")
        if not produces:
            continue
        teaches = ", ".join(ck.declared_ids(text, "teaches")) or "\u2014"
        rows.append(["[%s](%s)" % (ck.rel(bc, path), ck.rel(bc, path)), ", ".join(produces), teaches])
    if not rows:
        return "_No annotations found._"
    return ck.md_table(["File", "Evidences deliverable(s)", "Teaches"], rows, aligns=[":--", ":--", ":--"])


def block_tree(reg: Dict[str, Any], bc: str) -> str:
    lines = ["```text", "bootcamp/"]
    lines.extend(_walk_tree(bc, bc, prefix=""))
    lines.append("```")
    return "\n".join(lines)


def _walk_tree(root: str, path: str, prefix: str) -> List[str]:
    entries = []
    names = sorted(os.listdir(path))
    names = [n for n in names if n not in TREE_SKIP and not n.endswith(TREE_SKIP_SUFFIX)]
    # directories first, then files - both alphabetical
    dirs = [n for n in names if os.path.isdir(os.path.join(path, n))]
    files = [n for n in names if not os.path.isdir(os.path.join(path, n))]
    ordered = [("dir", n) for n in dirs] + [("file", n) for n in files]
    for idx, (kind, name) in enumerate(ordered):
        last = idx == len(ordered) - 1
        connector = "\u2514\u2500\u2500 " if last else "\u251c\u2500\u2500 "
        suffix = "/" if kind == "dir" else ""
        entries.append("%s%s%s%s" % (prefix, connector, name, suffix))
        if kind == "dir":
            extension = "    " if last else "\u2502   "
            entries.extend(_walk_tree(root, os.path.join(path, name), prefix + extension))
    return entries


BLOCKS = {
    "weeks": block_weeks,
    "gates": block_gates,
    "concepts": block_concepts,
    "deliverables": block_deliverables,
    "milestones": block_milestones,
    "grading": block_grading,
    "annotations": block_annotations,
    "tree": block_tree,
}


# --------------------------------------------------------------------------- #
def build(bc: str, reg: Dict[str, Any]) -> str:
    path = os.path.join(bc, SYLLABUS)
    text = ck.read_text(path)
    for name, builder in BLOCKS.items():
        body = builder(reg, bc)
        text = ck.replace_generated_block(text, name, body)
    return text


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 if syllabus.md is stale")
    parser.add_argument("--stdout", action="store_true", help="print instead of writing")
    args = parser.parse_args(argv)

    bc = ck.bootcamp_dir()
    reg = ck.load_registry()
    path = os.path.join(bc, SYLLABUS)

    if not os.path.exists(path):
        print("syllabus.md not found at %s" % path, file=sys.stderr)
        return 2

    original = ck.read_text(path)
    try:
        updated = build(bc, reg)
    except KeyError as exc:
        print("syllabus.md is missing a generated block: %s" % exc, file=sys.stderr)
        return 2

    if args.stdout:
        print(updated)
        return 0

    if args.check:
        if updated != original:
            print("syllabus.md is STALE - run: python bootcamp/tools/build_syllabus.py", file=sys.stderr)
            return 1
        print("syllabus.md is up to date")
        return 0

    if updated != original:
        ck.write_text(path, updated)
        print("syllabus.md regenerated")
    else:
        print("syllabus.md already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
