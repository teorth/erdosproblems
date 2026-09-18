#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from powerful_between_squares import ISSUE_PREFIX, h, is_powerful

def test_powerful():
    assert is_powerful(1)
    assert is_powerful(4)
    assert is_powerful(8)
    assert is_powerful(36)
    assert not is_powerful(12)
    assert not is_powerful(2)

def test_prefix():
    for n, want in enumerate(ISSUE_PREFIX, 1):
        assert h(n) == want, (n, h(n), want)

if __name__ == "__main__":
    test_powerful(); test_prefix(); print("ok - powerful between squares")
