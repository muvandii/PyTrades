#!/usr/bin/env python3
"""test_the_course.py - mutation-tests the course verifier.

A checker that cannot fail proves nothing. This script copies the bootcamp into
a temp directory, deliberately breaks one thing at a time, and asserts that
verify_course.py notices - and notices for the right reason.

Usage
-----
    python bootcamp/tools/test_the_course.py
"""

from __future__ import annotations

import os
import re
import shutil
import sys
import tempfile
import traceback
from typing import Callable, Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coursekit as ck  # noqa: E402
import verify_course as vc  # noqa: E402

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "generated")


def clone(bc: str) -> str:
    tmp = tempfile.mkdtemp(prefix="bootcamp-mutation-")
    shutil.copytree(bc, os.path.join(tmp, "bootcamp"), ignore=IGNORE)
    return os.path.join(tmp, "bootcamp")


def run_verifier(cloned_bc: str) -> Tuple[bool, List[str]]:
    """Run the verifier against a cloned bootcamp in a subprocess-like isolation."""
    reg = ck.load_registry(cloned_bc)
    rep = vc.run(cloned_bc, reg, quiet=True)
    return rep.failed(), rep.problems()


def read(path: str) -> str:
    return ck.read_text(path)


def write(path: str, text: str) -> None:
    ck.write_text(path, text)


# --------------------------------------------------------------------------- #
# mutations
# --------------------------------------------------------------------------- #
def m_delete_week(bc: str) -> None:
    os.remove(os.path.join(bc, "phases", "04-paper-replication", "week-08.md"))


def m_break_link(bc: str) -> None:
    path = os.path.join(bc, "syllabus.md")
    write(path, read(path).replace("phases/02-engine/week-03.md", "phases/02-engine/week-99.md"))


def m_strip_concept_format(bc: str) -> None:
    path = os.path.join(bc, "phases", "01-foundation", "concepts", "C01-returns-and-compounding.md")
    text = re.sub(r"\*\*DONE WHEN:\*\*.*", "", read(path))
    write(path, text)


def m_remove_days(bc: str) -> None:
    path = os.path.join(bc, "phases", "03-strategy-factory", "week-06.md")
    text = read(path)
    for day in ["Thu", "Fri", "Sat"]:
        text = re.sub(r"^#+ .*\b%s\b.*$(?:\n(?!^#).*)*" % day, "", text, flags=re.MULTILINE)
    write(path, text)


def m_detach_gate(bc: str) -> None:
    path = os.path.join(bc, "phases", "05-risk-portfolio", "week-10.md")
    write(path, re.sub(r"^#+ .*Gate.*$", "### Weekly wrap-up", read(path), flags=re.MULTILINE | re.IGNORECASE))


def m_registry_drift(bc: str) -> None:
    path = os.path.join(bc, "registry.json")
    import json

    reg = json.loads(read(path))
    reg["weeks"][0]["deliverables"] = ["D01", "D02", "D99"]
    reg["concepts"][0]["trigger"] = ""
    write(path, json.dumps(reg, indent=2))


def m_kill_graveyard(bc: str) -> None:
    os.remove(os.path.join(bc, "shared", "templates", "graveyard-entry.md"))


def m_stale_syllabus(bc: str) -> None:
    path = os.path.join(bc, "syllabus.md")
    write(path, read(path).replace("| Wk | Phase |", "| Wk | PHASE |", 1))


def m_break_python(bc: str) -> None:
    path = os.path.join(bc, "shared", "metrics-module", "kit", "metrics.py")
    write(path, read(path).replace("def ", "def broken(:\n", 1))


def m_drop_gate_check_doc(bc: str) -> None:
    path = os.path.join(bc, "phases", "06-live-paper", "gates", "week-11-gate.md")
    write(path, read(path).replace("G11.3", "CHECK-REMOVED"))


def m_strip_annotation(bc: str) -> None:
    path = os.path.join(bc, "phases", "05-risk-portfolio", "deliverables", "D15.md")
    write(path, re.sub(r"<!--\s*annotated:.*?-->", "", read(path), flags=re.DOTALL))


def m_strip_concept_link(bc: str) -> None:
    path = os.path.join(bc, "phases", "02-engine", "week-03.md")
    write(path, read(path).replace("concepts/C05-annualization.md", "concepts/C99-nope.md"))


def m_orphan_deliverable(bc: str) -> None:
    path = os.path.join(bc, "phases", "07-synthesis", "deliverables", "D18.md")
    write(path, read(path).replace("## Teaches", "## Some other heading"))


MUTATIONS: List[Tuple[str, Callable[[str], None], str]] = [
    ("clean copy passes", lambda bc: None, r""),
    ("delete a week file", m_delete_week, r"missing week file"),
    ("break an internal link", m_break_link, r"broken link|week-99"),
    ("strip a concept's DONE WHEN", m_strip_concept_format, r"DONE WHEN"),
    ("remove Thu-Sat tasks from a week", m_remove_days, r"no daily task for (Thu|Fri|Sat)"),
    ("detach a week's gate section", m_detach_gate, r"missing 'Gate' section"),
    ("drift the registry", m_registry_drift, r"unknown deliverable D99|no triggering failure"),
    ("delete the graveyard template", m_kill_graveyard, r"graveyard entry template"),
    ("let the syllabus go stale", m_stale_syllabus, r"stale"),
    ("break a python file", m_break_python, r"does not compile"),
    ("remove a gate check from its doc", m_drop_gate_check_doc, r"G11\.3"),
    ("strip an evidence annotation", m_strip_annotation, r"no annotated evidence file"),
    ("point a week at a missing concept", m_strip_concept_link, r"does not link concept C05|broken link"),
    ("rename a required deliverable section", m_orphan_deliverable, r"missing 'Teaches' section|does not restate"),
]


def main() -> int:
    bc = ck.bootcamp_dir()
    failures: List[str] = []
    print("=" * 78)
    print("mutation-testing the course verifier: %d scenarios" % len(MUTATIONS))
    print("=" * 78)

    for name, mutate, expect in MUTATIONS:
        clone_bc = clone(bc)
        try:
            mutate(clone_bc)
            failed, messages = run_verifier(clone_bc)
        except Exception:
            failures.append("%s: mutation harness crashed\n%s" % (name, traceback.format_exc()))
            continue
        finally:
            shutil.rmtree(os.path.dirname(clone_bc), ignore_errors=True)

        if expect == r"":
            # the untouched copy must pass
            if failed:
                failures.append("clean copy should pass but failed:\n      " + "\n      ".join(messages[:6]))
                print("FAIL  %s (verifier too strict: %d problems)" % (name, len(messages)))
            else:
                print("PASS  %s" % name)
            continue

        if not failed:
            failures.append("%s: verifier did not notice the breakage" % name)
            print("FAIL  %s (verifier blind to the mutation)" % name)
            continue
        hit = [m for m in messages if re.search(expect, m)]
        if not hit:
            failures.append(
                "%s: verifier failed, but not for the expected reason (%s)\n      got: %s"
                % (name, expect, " | ".join(messages[:4]))
            )
            print("FAIL  %s (wrong reason)" % name)
        else:
            print("PASS  %s -> %s" % (name, hit[0].strip()))

    print("-" * 78)
    if failures:
        print("VERIFIER NOT TRUSTWORTHY - %d scenarios failed" % len(failures))
        for f in failures:
            print("  - " + f)
        return 1
    print("VERIFIER TRUSTWORTHY - %d/%d mutation scenarios behaved" % (len(MUTATIONS), len(MUTATIONS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
