#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from min_circles import KNOWN, known_min_circles

def test_known():
    assert known_min_circles(4) == 4
    assert known_min_circles(5) == 5
    assert KNOWN[4] == 4

if __name__ == "__main__":
    test_known(); print("ok - min circles")
