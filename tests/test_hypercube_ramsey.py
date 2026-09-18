#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from hypercube_ramsey import KNOWN_EXACT, known_exact, q2_ramsey

def test_q2():
    assert q2_ramsey() == 6
    assert known_exact(2) == 6

def test_table():
    assert KNOWN_EXACT[1] == 2
    assert KNOWN_EXACT[2] == 6

if __name__ == "__main__":
    test_q2(); test_table(); print("ok - hypercube ramsey")
