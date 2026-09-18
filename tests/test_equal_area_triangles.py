#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from equal_area_triangles import KNOWN_LOWER, certified_lower_bounds, square_certificate

def test_square():
    assert square_certificate() == 4

def test_bounds():
    got = certified_lower_bounds()
    assert got[3] == 1
    assert got[4] == 4
    assert got[5] >= 4
    assert KNOWN_LOWER[4] == 4

if __name__ == "__main__":
    test_square(); test_bounds(); print("ok - equal area")
