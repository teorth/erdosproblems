#!/usr/bin/env python3
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oeis_cons_compare import compare_cons, digits_rounded, digits_truncated


def test_two_thirds_truncation_vs_rounding():
    # Issue #357 minimal reproduction: 2/3 to 15 digits.
    assert digits_truncated(Fraction(2, 3), 15) == "666666666666666"
    assert digits_rounded(Fraction(2, 3), 15) == "666666666666667"


def test_compare_detects_rounding_false_negative():
    oeis = "666666666666666"
    result = compare_cons(Fraction(2, 3), oeis)
    assert result["match"] is True
    assert result["rounding_false_negative"] is True
    assert result["rounded"] == "666666666666667"


def test_genuine_mismatch():
    result = compare_cons(Fraction(1, 7), "666666666666666")
    assert result["match"] is False
    assert result["rounding_false_negative"] is False


if __name__ == "__main__":
    test_two_thirds_truncation_vs_rounding()
    test_compare_detects_rounding_false_negative()
    test_genuine_mismatch()
    print("ok - oeis cons compare")
