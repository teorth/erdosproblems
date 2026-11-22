#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from derive_status import derive_state, expected_status


def test_ordinary_combination():
    assert derive_state("proved", "Lean") == "proved (Lean)"
    assert derive_state("open", "unformalized") == "open"
    assert derive_state("disproved", None) == "disproved"


def test_formal_annotation_without_an_informal_state_is_blank():
    assert derive_state("", "Lean") == ""
    assert derive_state(None, "Lean") == ""
    problem = {"formal_status": {"state": "Lean"}}
    assert expected_status(problem) == {}
