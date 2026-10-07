"""coursekit - shared helpers for the AI Trading Strategy Bootcamp tooling.

Stdlib only. Imported by build_syllabus.py and verify_course.py.

Annotation blocks
-----------------
Course files can declare machine-checked claims like this:

    <!-- annotated: produces=D01 -->
    <!-- /annotated -->

`produces=` names the deliverable ids the file is evidence for, `teaches=`
names what the file explains. verify_course.py checks that every annotated
block names things that exist in registry.json, and build_syllabus.py mirrors
the annotations into a human-readable cross-reference table in syllabus.md.

Everything else in this module is filesystem, front-matter and markdown
plumbing so the verifier and the generator agree on how files are read.
"""

from __future__ import annotations

import glob as _glob
import json
import os
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

ANNOTATION_RE = re.compile(r"<!--\s*annotated:(.*?)-->", re.DOTALL)
ANNOTATION_BLOCK_RE = re.compile(
    r"<!--\s*annotated:(?P<meta>.*?)-->(?P<body>.*?)<!--\s*/annotated\s*-->", re.DOTALL
)
GENERATED_BLOCK_RE = re.compile(
    r"(?P<open><!-- BEGIN:GENERATED (?P<name>[\w\-]+) -->)(?P<body>.*?)(?P<close><!-- END:GENERATED (?P=name) -->)",
    re.DOTALL,
)
LINK_RE = re.compile(r"\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"```")

REQUIRED_CONCEPT_HEADERS = [
    "WHY NOW",
    "FORMULA",
    "CODE",
    "EXAMPLE",
    "TIME",
    "DONE WHEN",
]

WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# --------------------------------------------------------------------------- #
# repo/registry
# --------------------------------------------------------------------------- #
def find_repo_root(start: Optional[str] = None) -> str:
    """Walk up until we find bootcamp/registry.json. Raise if not found."""
    path = os.path.abspath(start or os.path.dirname(os.path.abspath(__file__)))
    while True:
        candidate = os.path.join(path, "bootcamp", "registry.json")
        if os.path.isfile(candidate):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            raise RuntimeError(
                "could not locate bootcamp/registry.json above %s" % start
            )
        path = parent


def bootcamp_dir(root: Optional[str] = None) -> str:
    return os.path.join(find_repo_root(root), "bootcamp")


def load_registry(root: Optional[str] = None) -> Dict[str, Any]:
    with open(os.path.join(bootcamp_dir(root), "registry.json"), "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# --------------------------------------------------------------------------- #
# minimal front-matter parser (scalars, quoted scalars, inline [lists])
# --------------------------------------------------------------------------- #
_SCALAR = re.compile(r"^(?P<key>[A-Za-z_][\w\-]*)\s*:\s*(?P<value>.*?)\s*$")


def _parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw == "" or raw == "~" or raw.lower() == "null":
        return None
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [strip_quotes(p.strip()) for p in _split_top_level(inner)]
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d+\.\d+", raw):
        return float(raw)
    return strip_quotes(raw)


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _split_top_level(text: str) -> List[str]:
    parts, depth, current = [], 0, []
    for ch in text:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current))
    return parts


def parse_front_matter(text: str) -> Dict[str, Any]:
    """Parse a leading `---` front-matter block. Returns {} when absent."""
    if not text.startswith("---"):
        head = text.lstrip()
        if not head.startswith("---"):
            return {}
        text = head
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    body: List[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        body.append(line)
    else:
        return {}

    data: Dict[str, Any] = {}
    key: Optional[str] = None
    for line in body:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(("  -", "-", "\t-")):
            if key is None:
                continue
            item = line.strip().lstrip("-").strip()
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(_parse_scalar(item))
            continue
        match = _SCALAR.match(line)
        if match:
            key = match.group("key")
            data[key] = _parse_scalar(match.group("value"))
    return {k: v for k, v in data.items() if v is not None}


def front_matter_file(path: str) -> Dict[str, Any]:
    return parse_front_matter(read_text(path))


# --------------------------------------------------------------------------- #
# markdown helpers
# --------------------------------------------------------------------------- #
def headings(text: str) -> List[Tuple[int, str]]:
    out = []
    for m in HEADING_RE.finditer(strip_code(text)):
        out.append((len(m.group("level")), m.group("title").strip()))
    return out


def strip_code(text: str) -> str:
    """Blank out fenced code blocks so heading/link scans ignore code."""
    out, inside = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return "\n".join(out)


def sections(text: str, level: int = 2) -> List[str]:
    prefix = "#" * level + " "
    titles = []
    for line in strip_code(text).splitlines():
        if line.startswith(prefix) and not line.startswith(prefix + "#"):
            titles.append(line[len(prefix):].strip())
    return titles


def has_section(text: str, title: str, level: Optional[int] = None) -> bool:
    target = title.lower()
    for lvl, t in headings(text):
        if level is not None and lvl != level:
            continue
        if target in t.lower():
            return True
    return False


def links(text: str) -> List[str]:
    return [m.group("target") for m in LINK_RE.finditer(strip_code(text))]


def annotation_meta(text: str) -> List[Dict[str, str]]:
    metas = []
    for m in ANNOTATION_RE.finditer(text):
        raw = m.group(1).strip()
        meta: Dict[str, str] = {}
        for chunk in raw.split():
            if "=" in chunk:
                k, v = chunk.split("=", 1)
                meta[k.strip()] = v.strip()
        if meta:
            metas.append(meta)
    return metas


def declared_ids(text: str, key: str = "produces") -> List[str]:
    ids: List[str] = []
    for meta in annotation_meta(text):
        for value in meta.get(key, "").split(","):
            value = value.strip()
            if value and value not in ids:
                ids.append(value)
    return ids


def generated_blocks(text: str) -> List[Tuple[str, str]]:
    return [(m.group("name"), m.group("body")) for m in GENERATED_BLOCK_RE.finditer(text)]


def replace_generated_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(
        r"(<!-- BEGIN:GENERATED %s -->)(.*?)(<!-- END:GENERATED %s -->)" % (name, name),
        re.DOTALL,
    )
    if not pattern.search(text):
        raise KeyError("no generated block named %r" % name)
    def _sub(match: "re.Match[str]") -> str:
        return "%s\n%s\n%s" % (match.group(1), body.strip("\n"), match.group(3))

    return pattern.sub(_sub, text, count=1)


# --------------------------------------------------------------------------- #
# selection helpers
# --------------------------------------------------------------------------- #
def rel(root: str, path: str) -> str:
    return os.path.relpath(path, root).replace(os.sep, "/")


def glob_files(root: str, pattern: str) -> List[str]:
    return sorted(_glob.glob(os.path.join(root, pattern), recursive=True))


def by_week(registry: Dict[str, Any], week: int) -> Optional[Dict[str, Any]]:
    for w in registry["weeks"]:
        if w["n"] == week:
            return w
    return None


def delivers_for(registry: Dict[str, Any], concept_id: str) -> Optional[str]:
    for c in registry["concepts"]:
        if c["id"] == concept_id:
            return c.get("deliverable")
    return None


def concept_by_id(registry: Dict[str, Any], concept_id: str) -> Optional[Dict[str, Any]]:
    for c in registry["concepts"]:
        if c["id"] == concept_id:
            return c
    return None


def deliverable_by_id(registry: Dict[str, Any], deliverable_id: str) -> Optional[Dict[str, Any]]:
    for d in registry["deliverables"]:
        if d["id"] == deliverable_id:
            return d
    return None


def milestone_by_id(registry: Dict[str, Any], milestone_id: str) -> Optional[Dict[str, Any]]:
    for m in registry["milestones"]:
        if m["id"] == milestone_id:
            return m
    return None


def week_path(bc: str, week: Dict[str, Any]) -> str:
    phase_dir = next(p["dir"] for p in load_registry_for(bc)["phases"] if p["id"] == week["phase"])
    return os.path.join(bc, "phases", phase_dir, "week-%02d.md" % week["n"])


_registry_cache: Dict[str, Dict[str, Any]] = {}


def load_registry_for(bc: str) -> Dict[str, Any]:
    if bc not in _registry_cache:
        with open(os.path.join(bc, "registry.json"), "r", encoding="utf-8") as fh:
            _registry_cache[bc] = json.load(fh)
    return _registry_cache[bc]


# --------------------------------------------------------------------------- #
# table rendering
# --------------------------------------------------------------------------- #
def md_table(headers: Sequence[str], rows: Iterable[Sequence[Any]], aligns: Optional[Sequence[str]] = None) -> str:
    headers = list(headers)
    rows = [[("" if cell is None else str(cell)) for cell in row] for row in rows]
    aligns = list(aligns or ["---"] * len(headers))
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def truncate(text: str, width: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= width:
        return text
    return text[: width - 1].rstrip() + "\u2026"
