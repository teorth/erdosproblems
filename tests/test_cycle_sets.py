#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from cycle_sets import KNOWN, cycle_lengths, f

def test_triangle():
    assert cycle_lengths(3, {(0,1),(1,2),(2,0)}) == frozenset({3})
    assert cycle_lengths(3, set()) == frozenset()

def test_known():
    for n, want in KNOWN.items():
        assert f(n) == want, (n, f(n), want)

if __name__ == "__main__":
    test_triangle(); test_known(); print("ok - cycle sets")
