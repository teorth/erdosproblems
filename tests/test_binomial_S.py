#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from binomial_S import ISSUE_PREFIX, S, digit_sum, max_exponent, valuation_binom


def test_digit_sum():
    assert digit_sum(9, 2) == 2  # 1001_2
    assert digit_sum(70, 5) == 6  # 240_5


def test_valuation_examples():
    # C(9,2) = 36 = 2^2 * 3^2, so v_2 = 2 and v_3 = 2
    assert valuation_binom(9, 2, 2) == 2
    assert valuation_binom(9, 2, 3) == 2
    # C(8,4) = 70 = 2 * 5 * 7
    assert valuation_binom(8, 4, 2) == 1
    assert max_exponent(8, 4) == 1


def test_S_rejects_n_below_two():
    try:
        S(1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_S_prefix_issue_354():
    # n = 2 .. 40 as listed in issue 354
    got = [S(n) for n in range(2, 41)]
    assert got == ISSUE_PREFIX


if __name__ == "__main__":
    test_digit_sum()
    test_valuation_examples()
    test_S_rejects_n_below_two()
    test_S_prefix_issue_354()
    print("ok - S(n)")
