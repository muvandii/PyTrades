"""Tests for the spine's command-line surface (kit-only; NOT part of the engine contract).

`make list`, `make run` and friends are the first things a student touches, so their
plumbing is tested here. The cross-engine contract lives in test_spine_contract.py.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kit import spine  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _write_spec(config_dir, spec_id: str, **overrides) -> str:
    payload = {
        "id": spec_id,
        "name": "test spec",
        "universe": ["SPY"],
        "params": {},
        "thesis": "test thesis with a mechanism",
        "tags": ["test"],
        "long_only": True,
        "max_gross_exposure": 1.0,
        "rebalance": "daily",
    }
    payload.update(overrides)
    path = os.path.join(config_dir, "%s.json" % spec_id)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle)
    return path


def test_list_specs_reads_from_the_config_dir(tmp_path):
    """Regression: list_specs used to resolve 'X.json' against the cwd, not config/."""
    _write_spec(str(tmp_path), "S01_test")
    _write_spec(str(tmp_path), "S02_test")
    specs = spine.list_specs(str(tmp_path))
    assert [s.id for s in specs] == ["S01_test", "S02_test"]
    assert specs[0].universe == ["SPY"]


def test_list_specs_survives_a_broken_file(tmp_path, capsys):
    _write_spec(str(tmp_path), "S01_ok")
    with open(os.path.join(str(tmp_path), "S02_broken.json"), "w", encoding="utf-8") as handle:
        handle.write("{not json at all")
    specs = spine.list_specs(str(tmp_path))
    captured = capsys.readouterr()
    assert [s.id for s in specs] == ["S01_ok"]
    assert "S02_broken.json" in captured.err, "a broken spec must be reported by name"


def test_list_specs_returns_empty_when_config_dir_is_missing(tmp_path):
    assert spine.list_specs(str(tmp_path / "nope")) == []


def test_cli_list_runs_from_the_repo_root_with_an_empty_config(tmp_path):
    env = dict(os.environ, PYTRADES_CONFIG=str(tmp_path))
    proc = subprocess.run(
        [sys.executable, "-m", "kit.spine", "list"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "no specs in config/" in proc.stdout


def test_validate_rejects_a_spec_file_without_a_thesis(tmp_path):
    """A spec file must carry a thesis; the in-memory dataclass stays lenient so
    programmatic test fixtures (and the contract suite) can build minimal specs."""
    path = _write_spec(str(tmp_path), "S01_nothesis", thesis="")
    with pytest.raises(ValueError):
        spine.load_spec(path)
    assert spine.load_spec(_write_spec(str(tmp_path), "S01_thesis")).id == "S01_thesis"
