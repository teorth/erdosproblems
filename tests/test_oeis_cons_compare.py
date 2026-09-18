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



def test_truncation_does_not_round_across_a_power_of_ten():
    value = Fraction(10**40 - 1, 10**40)
    assert digits_truncated(value, 8) == '99999999'
    assert digits_rounded(value, 8) == '10000000'


def test_rounding_uses_the_exact_halfway_comparison():
    halfway = Fraction(12345, 10000)
    epsilon = Fraction(1, 10**50)
    assert digits_rounded(halfway - epsilon, 4) == '1234'
    assert digits_rounded(halfway, 4) == '1235'
    assert digits_rounded(halfway + epsilon, 4) == '1235'


def test_significant_digits_outside_float_range():
    for value in (Fraction(10**400), Fraction(1, 10**400)):
        assert digits_truncated(value, 8) == '10000000'
        assert digits_rounded(value, 8) == '10000000'


def test_comparison_does_not_change_decimal_context():
    from decimal import localcontext
    with localcontext() as context:
        context.prec = 7
        compare_cons(Fraction(2, 3), '66666666')
        assert context.prec == 7


if __name__ == "__main__":
    test_two_thirds_truncation_vs_rounding()
    test_compare_detects_rounding_false_negative()
    test_genuine_mismatch()
    test_truncation_does_not_round_across_a_power_of_ten()
    test_rounding_uses_the_exact_halfway_comparison()
    test_significant_digits_outside_float_range()
    test_comparison_does_not_change_decimal_context()
    print("ok - oeis cons compare (7 tests)")
