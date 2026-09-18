#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from equal_lcm_triple_free import ISSUE_PREFIX, f, is_triple_free

def test_small_exhaustive():
    for n, want in enumerate(ISSUE_PREFIX[:20], 1):
        assert f(n) == want, (n, f(n), want)

def test_witness():
    assert is_triple_free([1,2,3,4,5])
    assert not is_triple_free([2,3,6])  # lcm 6

if __name__ == "__main__":
    test_witness(); test_small_exhaustive(); print("ok - equal lcm triple-free")
