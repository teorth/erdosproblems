#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from multiplicative_sidon import F, KNOWN, is_multiplicative_sidon


def test_known_table():
    for n, val in KNOWN.items():
        assert F(n) == val, (n, F(n), val)


def test_small_witnesses():
    assert is_multiplicative_sidon([1, 2, 3, 4, 5])
    assert not is_multiplicative_sidon([1, 2, 3, 4, 5, 6])  # 2*6=3*4
    assert F(6) == 5


def test_monotonic():
    prev = 0
    for n in range(1, 17):
        v = F(n)
        assert v >= prev
        prev = v


if __name__ == "__main__":
    test_known_table()
    test_small_witnesses()
    test_monotonic()
    print("ok - multiplicative Sidon F(n)")
