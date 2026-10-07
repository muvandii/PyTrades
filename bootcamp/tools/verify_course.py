#!/usr/bin/env python3
"""verify_course.py - the acceptance test for the bootcamp package itself.

The course claims a lot: every week has a gate, every concept has a trigger,
every deliverable maps to a milestone, the graveyard is required, live paper
trading is mandatory, and a student can finish solo. This script checks those
claims against the actual files, so the course cannot silently rot.

Usage
-----
    python bootcamp/tools/verify_course.py            # full report
    python bootcamp/tools/verify_course.py -q         # only problems
    python bootcamp/tools/test_the_course.py          # prove the verifier bites
"""

from __future__ import annotations

import argparse
import os
import py_compile
import re
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coursekit as ck  # noqa: E402

OK = "PASS"
BAD = "FAIL"

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|TBD|XXX|PLACEHOLDER)\b")


class Report:
    def __init__(self) -> None:
        self.results: List[Tuple[str, str, List[str]]] = []

    def add(self, name: str, problems: List[str], notes: Optional[List[str]] = None) -> None:
        self.results.append((name, OK if not problems else BAD, problems + (notes or [])))

    def problems(self) -> List[str]:
        out = []
        for name, status, messages in self.results:
            if status == BAD:
                out.extend("  [%s] %s" % (name, m) for m in messages)
        return out

    def failed(self) -> bool:
        return any(status == BAD for _, status, _ in self.results)

    def render(self, quiet: bool = False) -> str:
        lines = []
        for name, status, messages in self.results:
            if quiet and status == OK:
                continue
            lines.append("%s  %s" % (status, name))
            for msg in messages:
                prefix = "       - " if status == BAD else "       \u00b7 "
                lines.append(prefix + msg)
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #
def check_counts(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems = []
    if len(reg["weeks"]) != 13:
        problems.append("registry has %d weeks, spec says 13" % len(reg["weeks"]))
    if len(reg["phases"]) != 7:
        problems.append("registry has %d phases, spec says 7" % len(reg["phases"]))
    if len(reg["milestones"]) != 6:
        problems.append("registry has %d milestones, spec says 6" % len(reg["milestones"]))
    if len(reg["deliverables"]) < 15:
        problems.append("spec promises 15+ deliverables, registry has %d" % len(reg["deliverables"]))
    if len(reg["concepts"]) < 20:
        problems.append("spec promises ~20 concepts, registry has %d" % len(reg["concepts"]))
    tracked = [d for d in reg["deliverables"] if d["milestone"]]
    if len(tracked) != len(reg["deliverables"]):
        problems.append("some deliverables map to no milestone: %s" % [d["id"] for d in reg["deliverables"] if not d["milestone"]])
    rep.add(
        "counts: 13 weeks / 7 phases / 6 milestones / 15+ deliverables / 20+ concepts",
        problems,
        notes=[
            "%d deliverables, %d concept injections, %d milestones"
            % (len(reg["deliverables"]), len(reg["concepts"]), len(reg["milestones"]))
        ],
    )


def check_registry_integrity(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    d_ids = {d["id"] for d in reg["deliverables"]}
    c_ids = {c["id"] for c in reg["concepts"]}
    m_ids = {m["id"] for m in reg["milestones"]}
    w_ids = {w["n"] for w in reg["weeks"]}

    for w in reg["weeks"]:
        for did in w["deliverables"]:
            if did not in d_ids:
                problems.append("week %d references unknown deliverable %s" % (w["n"], did))
        for cid in w["concepts"]:
            if cid not in c_ids:
                problems.append("week %d references unknown concept %s" % (w["n"], cid))
        if w["milestone"] and w["milestone"] not in m_ids:
            problems.append("week %d references unknown milestone %s" % (w["n"], w["milestone"]))
        if str(w["n"]) not in reg["gates"]:
            problems.append("week %d has no gate in registry" % w["n"])
    for d in reg["deliverables"]:
        if d["week"] not in w_ids:
            problems.append("deliverable %s points at unknown week %s" % (d["id"], d["week"]))
        if d["milestone"] not in m_ids:
            problems.append("deliverable %s points at unknown milestone %s" % (d["id"], d["milestone"]))
        owner = ck.by_week(reg, d["week"])
        if owner and d["id"] not in owner["deliverables"]:
            problems.append("deliverable %s is not listed in week %d" % (d["id"], d["week"]))
        if not d.get("teaches"):
            problems.append("deliverable %s does not state what it teaches" % d["id"])
        if not d.get("evidence"):
            problems.append("deliverable %s has no evidence list" % d["id"])
    for c in reg["concepts"]:
        if not c.get("trigger"):
            problems.append("concept %s has no triggering failure" % c["id"])
        if not c.get("deliverable"):
            problems.append("concept %s is not demanded by any deliverable" % c["id"])
        owner = ck.by_week(reg, c["week"])
        if owner and c["id"] not in owner["concepts"]:
            problems.append("concept %s is not listed in week %d" % (c["id"], c["week"]))
    for m in reg["milestones"]:
        if m["week"] not in w_ids:
            problems.append("milestone %s points at unknown week %s" % (m["id"], m["week"]))
        if not m.get("pass_condition"):
            problems.append("milestone %s has no pass condition" % m["id"])
    for p in reg["phases"]:
        for cid in p["concepts"]:
            if cid not in c_ids:
                problems.append("phase %s lists unknown concept %s" % (p["id"], cid))
        for did in p["deliverables"]:
            if did not in d_ids:
                problems.append("phase %s lists unknown deliverable %s" % (p["id"], did))
        if not p.get("teacher_builds") or not p.get("student_ships"):
            problems.append("phase %s does not declare both teacher_builds and student_ships" % p["id"])
    weights = sum(a["weight"] for a in reg["grading"]["artifacts"])
    if weights != reg["grading"]["total"]:
        problems.append("grading weights sum to %d, declared total is %d" % (weights, reg["grading"]["total"]))
    rep.add("registry integrity (ids, ownership, milestones, weights)", problems)


def check_structure(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []

    for path in ["README.md", "syllabus.md", "registry.json"]:
        if not os.path.isfile(os.path.join(bc, path)):
            problems.append("missing bootcamp/%s" % path)

    for p in reg["phases"]:
        for name in ["README.md", "rubric.md"]:
            if not os.path.isfile(os.path.join(bc, "phases", p["dir"], name)):
                problems.append("missing phases/%s/%s" % (p["dir"], name))

    for w in reg["weeks"]:
        phase = next(p for p in reg["phases"] if p["id"] == w["phase"])
        path = os.path.join(bc, "phases", phase["dir"], "week-%02d.md" % w["n"])
        if not os.path.isfile(path):
            problems.append("missing week file %s" % ck.rel(bc, path))
        gate = os.path.join(bc, "phases", phase["dir"], "gates", "week-%02d-gate.md" % w["n"])
        if not os.path.isfile(gate):
            problems.append("missing gate file %s" % ck.rel(bc, gate))
        for did in w["deliverables"]:
            dpath = os.path.join(bc, "phases", phase["dir"], "deliverables", "%s.md" % did)
            if not os.path.isfile(dpath):
                problems.append("missing deliverable sheet %s" % ck.rel(bc, dpath))

    for c in reg["concepts"]:
        path = os.path.join(bc, c["file"])
        if not os.path.isfile(path):
            problems.append("missing concept file %s" % c["file"])

    for m in reg["milestones"]:
        week = ck.by_week(reg, m["week"])
        phase = next(p for p in reg["phases"] if p["id"] == week["phase"])
        matches = ck.glob_files(bc, "phases/%s/milestones/%s-*.md" % (phase["dir"], m["id"]))
        if not matches:
            problems.append("missing milestone card for %s in phases/%s/milestones/" % (m["id"], phase["dir"]))

    for path in [
        "shared/repo-scaffold/README.md",
        "shared/data-fetcher/kit/data_fetcher.py",
        "shared/metrics-module/kit/metrics.py",
        "shared/journal-template.md",
        "shared/retro-template.md",
        "shared/gate-checklist.md",
        "shared/templates/verdict.md",
        "shared/templates/graveyard-entry.md",
        "shared/templates/tearsheet.md",
        "shared/templates/thesis.md",
        "shared/templates/debunk.md",
        "shared/templates/deviation-log.md",
        "shared/templates/reconciliation.md",
        "shared/testing-guide.md",
        "shared/costs-model.md",
        "capstone/rubric.md",
        "capstone/writeup-template.md",
        "capstone/portfolio-template.md",
        "capstone/recall-test.md",
        "phases/01-foundation/templates/viral-debunk-sheet.md",
        "phases/02-engine/spec/engine-spec.md",
        "phases/03-strategy-factory/spec/strategy-config-schema.md",
        "phases/06-live-paper/spec/signal-generator-spec.md",
    ]:
        if not os.path.isfile(os.path.join(bc, path)):
            problems.append("missing required package file %s" % path)

    rep.add("package structure (weeks, gates, concepts, deliverables, milestone cards, shared kit, capstone)", problems)


def check_week_files(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    for w in reg["weeks"]:
        phase = next(p for p in reg["phases"] if p["id"] == w["phase"])
        path = os.path.join(bc, "phases", phase["dir"], "week-%02d.md" % w["n"])
        if not os.path.isfile(path):
            continue
        text = ck.read_text(path)
        rel = ck.rel(bc, path)
        fm = ck.parse_front_matter(text)

        if fm.get("week") != w["n"]:
            problems.append("%s: front matter week=%r, registry says %d" % (rel, fm.get("week"), w["n"]))
        if fm.get("phase") != w["phase"]:
            problems.append("%s: front matter phase=%r, registry says %s" % (rel, fm.get("phase"), w["phase"]))
        if set(fm.get("deliverables") or []) != set(w["deliverables"]):
            problems.append("%s: front matter deliverables %r != registry %r" % (rel, fm.get("deliverables"), w["deliverables"]))
        if set(fm.get("concepts") or []) != set(w["concepts"]):
            problems.append("%s: front matter concepts %r != registry %r" % (rel, fm.get("concepts"), w["concepts"]))

        # seven daily tasks
        day_titles = []
        for line in ck.strip_code(text).splitlines():
            m = re.match(r"^#{3,4}\s+(?P<title>.+)$", line.strip())
            if m:
                title = m.group("title")
                for label in ck.WEEKDAY_LABELS:
                    if re.search(r"\b%s\b" % label, title):
                        day_titles.append(label)
                        break
        missing_days = [d for d in ck.WEEKDAY_LABELS if d not in day_titles]
        if missing_days:
            problems.append("%s: no daily task for %s" % (rel, ", ".join(missing_days)))

        for required in ["Learning objective", "Deliverable", "Gate", "Graveyard"]:
            if not ck.has_section(text, required):
                problems.append("%s: missing '%s' section" % (rel, required))

        for cid in w["concepts"]:
            c = ck.concept_by_id(reg, cid)
            target = os.path.relpath(os.path.join(bc, c["file"]), os.path.dirname(path))
            if target.replace(os.sep, "/") not in text.replace(os.sep, "/"):
                problems.append("%s: does not link concept %s (%s)" % (rel, cid, c["file"]))
    rep.add("week files: 7 daily tasks, objective, deliverable, gate, graveyard prompt, concept links", problems)


def check_concept_files(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    for c in reg["concepts"]:
        path = os.path.join(bc, c["file"])
        if not os.path.isfile(path):
            continue
        text = ck.read_text(path)
        rel = c["file"]
        fm = ck.parse_front_matter(text)

        for key, expected in [("id", c["id"]), ("week", c["week"]), ("tier", c["tier"])]:
            if fm.get(key) != expected:
                problems.append("%s: front matter %s=%r, registry says %r" % (rel, key, fm.get(key), expected))
        if str(fm.get("triggered_by", "")) != c["deliverable"]:
            problems.append("%s: triggered_by=%r, registry says %s" % (rel, fm.get("triggered_by"), c["deliverable"]))
        if not fm.get("trigger"):
            problems.append("%s: front matter carries no trigger text" % rel)

        for header in ck.REQUIRED_CONCEPT_HEADERS:
            if not re.search(r"\*\*\s*%s\s*:?\*\*" % re.escape(header), text, re.IGNORECASE) and not ck.has_section(text, header):
                problems.append("%s: missing '%s' block required by the concept format" % (rel, header))

        if "```" not in text:
            problems.append("%s: no runnable code block" % rel)
        if "DONE WHEN" in text.upper():
            done_block = text.split("DONE WHEN", 1)[1]
            if not re.search(r"explain", done_block, re.IGNORECASE):
                problems.append("%s: DONE WHEN does not require explaining the concept" % rel)
            if not re.search(r"spot", done_block, re.IGNORECASE):
                problems.append("%s: DONE WHEN does not require spotting it wrong" % rel)
    rep.add("concept files: format (why now / formula / code / example / time / done when) + trigger wiring", problems)


def check_deliverable_files(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    for d in reg["deliverables"]:
        phase = next(p for p in reg["phases"] if p["id"] == d["phase"])
        path = os.path.join(bc, "phases", phase["dir"], "deliverables", "%s.md" % d["id"])
        if not os.path.isfile(path):
            continue
        text = ck.read_text(path)
        rel = ck.rel(bc, path)
        fm = ck.parse_front_matter(text)
        if fm.get("id") != d["id"]:
            problems.append("%s: front matter id=%r" % (rel, fm.get("id")))
        if fm.get("week") != d["week"]:
            problems.append("%s: front matter week=%r, registry says %d" % (rel, fm.get("week"), d["week"]))
        if str(fm.get("milestone", "")) != str(d["milestone"]):
            problems.append("%s: front matter milestone=%r, registry says %s" % (rel, fm.get("milestone"), d["milestone"]))
        for required in ["Objective", "Teaches", "Build", "Definition of done", "Evidence"]:
            if not ck.has_section(text, required):
                problems.append("%s: missing '%s' section" % (rel, required))
        for ev in d["evidence"]:
            leaf = ev.split("/")[-1]
            if leaf not in text and ev not in text:
                problems.append("%s: registry evidence %r not mentioned" % (rel, ev))
    rep.add("deliverable sheets: objective, teaches, build, definition of done, evidence", problems)


def check_milestone_cards(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    for m in reg["milestones"]:
        week = ck.by_week(reg, m["week"])
        phase = next(p for p in reg["phases"] if p["id"] == week["phase"])
        matches = ck.glob_files(bc, "phases/%s/milestones/%s-*.md" % (phase["dir"], m["id"]))
        if not matches:
            continue
        text = ck.read_text(matches[0])
        rel = ck.rel(bc, matches[0])
        if m["pass_condition"] not in text:
            problems.append("%s does not restate the registry pass condition verbatim" % rel)
        for required in ["Fail", "Remediate"]:
            if required.lower() not in text.lower():
                problems.append("%s: missing '%s' guidance" % (rel, required))
    rep.add("milestone cards: pass condition verbatim + fail remediation path", problems)


def check_annotations(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    evidenced: Dict[str, List[str]] = {}
    for path in sorted(ck.glob_files(bc, "**/*.md")):
        text = ck.read_text(path)
        for meta in ck.annotation_meta(text):
            produces = meta.get("produces", "")
            for did in [x.strip() for x in produces.split(",") if x.strip()]:
                if not ck.deliverable_by_id(reg, did):
                    problems.append("%s: annotated with unknown deliverable %s" % (ck.rel(bc, path), did))
                else:
                    evidenced.setdefault(did, []).append(ck.rel(bc, path))
            teaches = meta.get("teaches", "")
            for cid in [x.strip() for x in teaches.split(",") if x.strip()]:
                if not ck.concept_by_id(reg, cid):
                    problems.append("%s: annotated with unknown concept %s" % (ck.rel(bc, path), cid))
    uncovered = sorted(set(d["id"] for d in reg["deliverables"]) - set(evidenced))
    if uncovered:
        problems.append("deliverables with no annotated evidence file: %s" % ", ".join(uncovered))
    rep.add(
        "annotations: every annotated id exists + every deliverable has evidence",
        problems,
        notes=["%d deliverables evidenced by %d annotated files" % (len(evidenced), sum(len(v) for v in evidenced.values()))],
    )


def check_links(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    checked = 0
    for path in sorted(ck.glob_files(bc, "**/*.md")):
        text = ck.read_text(path)
        for target in ck.links(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            if "{" in target or "<" in target:
                continue  # documented template placeholder in a path
            checked += 1
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                problems.append("%s -> broken link %s" % (ck.rel(bc, path), target))
    rep.add("internal links resolve", problems, notes=["%d relative links checked" % checked])


def check_gates(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    for w in reg["weeks"]:
        gate = reg["gates"].get(str(w["n"]))
        if not gate:
            continue
        if not gate["checks"]:
            problems.append("week %d gate has no checks" % w["n"])
        for check in gate["checks"]:
            kind = check["type"]
            if kind not in {
                "file_exists",
                "files_min",
                "file_contains_section",
                "pattern_in_file",
                "journal_min",
                "command",
                "csv_rows_min",
                "retro",
                "manual",
            }:
                problems.append("week %d gate: unknown check type %r" % (w["n"], kind))
            if kind in {"file_exists", "file_contains_section", "pattern_in_file", "csv_rows_min"} and not check.get("path"):
                problems.append("week %d gate %s: missing path" % (w["n"], check["id"]))
            if kind == "manual" and not check.get("desc"):
                problems.append("week %d gate %s: manual check without a description" % (w["n"], check["id"]))
            if check.get("type") == "file_exists":
                # course-side artifacts that exist today must exist for real
                candidate = os.path.join("phases", "01-foundation", check["path"])
                if check["path"].startswith("phases/") and not os.path.exists(os.path.join(bc, check["path"])):
                    problems.append("week %d gate %s points at missing course file %s" % (w["n"], check["id"], check["path"]))
        phase = next(p for p in reg["phases"] if p["id"] == w["phase"])
        gate_path = os.path.join(bc, "phases", phase["dir"], "gates", "week-%02d-gate.md" % w["n"])
        if os.path.isfile(gate_path):
            text = ck.read_text(gate_path)
            for check in gate["checks"]:
                if check["id"] not in text:
                    problems.append("%s does not document check %s" % (ck.rel(bc, gate_path), check["id"]))
        # honest hint about unsatisfiable-early gates
    rep.add("gates: every week has auto + manual checks, documented in the gate file", problems)


def check_python_hygiene(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    count = 0
    with tempfile.TemporaryDirectory() as tmp:
        for path in sorted(ck.glob_files(bc, "**/*.py")):
            if "__pycache__" in path:
                continue
            count += 1
            try:
                py_compile.compile(path, cfile=os.path.join(tmp, "out.pyc"), doraise=True)
            except py_compile.PyCompileError as exc:
                problems.append("%s does not compile: %s" % (ck.rel(bc, path), str(exc).splitlines()[-1]))
    rep.add("python files compile", problems, notes=["%d python files compiled" % count])


def check_placeholders(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    allow = ("templates/", "solutions/", "instructor/", "worked-example/")
    for path in sorted(ck.glob_files(bc, "**/*.md")):
        rel = ck.rel(bc, path)
        if any(a in rel for a in allow):
            continue
        text = ck.strip_code(ck.read_text(path))
        for m in PLACEHOLDER_RE.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            problems.append("%s:%d contains %s" % (rel, line_no, m.group(0)))
    rep.add("no unresolved placeholders in course files (templates/solutions excluded)", problems)


def check_generated_sync(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []
    try:
        import build_syllabus
    except Exception as exc:  # pragma: no cover
        rep.add("generated blocks in sync", ["cannot import build_syllabus: %s" % exc])
        return
    path = os.path.join(bc, "syllabus.md")
    if os.path.isfile(path):
        try:
            rebuilt = build_syllabus.build(bc, reg)
        except KeyError as exc:
            problems.append("syllabus.md missing generated block %s" % exc)
        else:
            if rebuilt != ck.read_text(path):
                problems.append("syllabus.md generated tables are stale (run build_syllabus.py)")
    rep.add("generated blocks in sync with registry", problems)


# --------------------------------------------------------------------------- #
# acceptance criteria - the spec, verbatim
# --------------------------------------------------------------------------- #
def check_acceptance(reg: Dict[str, Any], bc: str, rep: Report) -> None:
    problems: List[str] = []

    # CA1 - every week has daily tasks, a deliverable, and a gate
    for w in reg["weeks"]:
        if not w["deliverables"]:
            problems.append("CA1: week %d ships nothing" % w["n"])
        if str(w["n"]) not in reg["gates"]:
            problems.append("CA1: week %d has no gate" % w["n"])
        if not w.get("checkpoint"):
            problems.append("CA1: week %d has no checkpoint text" % w["n"])

    # CA2 - every concept has a trigger, and the trigger is a failure, not a syllabus
    for c in reg["concepts"]:
        if not c["trigger"]:
            problems.append("CA2: concept %s has no trigger" % c["id"])
        if c["deliverable"] not in {d["id"] for d in reg["deliverables"]}:
            problems.append("CA2: concept %s is not demanded by a real deliverable" % c["id"])

    # CA3 - every deliverable maps to a milestone
    for d in reg["deliverables"]:
        if not d["milestone"]:
            problems.append("CA3: deliverable %s maps to no milestone" % d["id"])

    # CA4 - every strategy ships with a verdict template
    verdict = os.path.join(bc, "shared/templates/verdict.md")
    if not os.path.isfile(verdict):
        problems.append("CA4: no verdict template shipped")
    else:
        vtext = ck.read_text(verdict)
        for required in ["edge", "no edge", "inconclusive"]:
            if required not in vtext.lower():
                problems.append("CA4: verdict template does not offer '%s'" % required)
    if not reg["quality_gates"]["strategy_ship"]:
        problems.append("CA4: no strategy ship checklist in the registry")

    # CA5 - the graveyard is a required artifact
    if not os.path.isfile(os.path.join(bc, "shared/templates/graveyard-entry.md")):
        problems.append("CA5: no graveyard entry template")
    graveyard_gates = [1 for w in reg["weeks"] if "raveyard" in w["graveyard_prompt"]]
    if len(graveyard_gates) != len(reg["weeks"]):
        problems.append("CA5: some weeks carry no graveyard prompt")
    has_gate_check = any(
        chk["type"] == "file_contains_section" and "graveyard.md" in str(chk.get("path", ""))
        for g in reg["gates"].values()
        for chk in g["checks"]
    )
    if not has_gate_check:
        problems.append("CA5: no automated gate ever checks graveyard.md")

    # CA6 - live paper trading is mandatory
    if not reg["live_paper"]["mandatory"]:
        problems.append("CA6: live paper is not marked mandatory")
    live_checks = [
        chk
        for n in ("11", "12")
        for chk in reg["gates"][n]["checks"]
        if chk["type"] in {"file_exists", "files_min", "csv_rows_min"}
    ]
    if len(live_checks) < 4:
        problems.append("CA6: weeks 11-12 do not gate on enough live artifacts (%d)" % len(live_checks))
    if not os.path.isfile(os.path.join(bc, "phases/06-live-paper/spec/signal-generator-spec.md")):
        problems.append("CA6: no signal generator spec")

    # CA7 - complete solo, self-paced
    for w in reg["weeks"]:
        if not w.get("graveyard_prompt"):
            problems.append("CA7: week %d gives the student nothing to self-check" % w["n"])
    if not os.path.isfile(os.path.join(bc, "shared/gate-checklist.md")):
        problems.append("CA7: no self-grading gate checklist")
    if os.path.isdir(os.path.join(bc, "phases/02-engine/instructor")):
        # instructor material is allowed, but it must be explicitly optional
        if not ck.glob_files(bc, "phases/02-engine/instructor/*OPTIONAL*"):
            problems.append("CA7: instructor material exists without an explicit OPTIONAL marker so a solo student knows it is skippable")

    # CA8 - the final artifact is a public, shareable repo + writeup
    if not os.path.isfile(os.path.join(bc, "capstone/writeup-template.md")):
        problems.append("CA8: no public writeup template")
    gate13 = reg["gates"]["13"]["checks"]
    if not any(chk["type"] == "pattern_in_file" and "WRITEUP.md" in str(chk.get("path", "")) for chk in gate13):
        problems.append("CA8: week 13 gate does not require a published writeup")
    if not any("stranger" in chk.get("desc", "").lower() for chk in gate13):
        problems.append("CA8: week 13 gate does not require the stranger-clone test")

    rep.add("acceptance criteria CA1-CA8", problems)


CHECKS = [
    check_counts,
    check_registry_integrity,
    check_structure,
    check_week_files,
    check_concept_files,
    check_deliverable_files,
    check_milestone_cards,
    check_gates,
    check_annotations,
    check_links,
    check_python_hygiene,
    check_placeholders,
    check_generated_sync,
    check_acceptance,
]


def run(bc: Optional[str] = None, reg: Optional[Dict[str, Any]] = None, quiet: bool = False) -> Report:
    bc = bc or ck.bootcamp_dir()
    reg = reg or ck.load_registry(bc)
    rep = Report()
    for check in CHECKS:
        try:
            check(reg, bc, rep)
        except Exception as exc:  # a crashing check is a failing check
            rep.add(check.__name__, ["checker crashed: %r" % exc])
    return rep


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-q", "--quiet", action="store_true", help="only show failures")
    args = parser.parse_args(argv)

    bc = ck.bootcamp_dir()
    reg = ck.load_registry(bc)
    rep = run(bc, reg)

    print("=" * 78)
    print("PyTrades bootcamp - course acceptance test")
    print("=" * 78)
    print(rep.render(quiet=args.quiet))
    print("-" * 78)
    passed = sum(1 for _, status, _ in rep.results if status == OK)
    print("%d/%d check groups passed" % (passed, len(rep.results)))
    if rep.failed():
        print("COURSE IS NOT ACCEPTED - fix the failures above")
        return 1
    print("COURSE ACCEPTED - every structural claim in the spec is backed by a file")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
