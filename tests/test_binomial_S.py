#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from binomial_S import S, binomial, largest_prime_power_exponent


def test_binom_small():
    assert binomial(9, 1) == 9
    assert binomial(9, 2) == 36
    assert binomial(8, 4) == 70


def test_exponent_examples():
    assert largest_prime_power_exponent(9) == 2
    assert largest_prime_power_exponent(70) == 1
    assert largest_prime_power_exponent(8) == 3


def test_S_rejects_n_below_two():
    try:
        S(1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_S_prefix_issue_354():
    # n = 2 .. 32 as listed in issue 354
    got = [S(n) for n in range(2, 33)]
    expected = [
        1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2,
    ]
    assert got == expected


if __name__ == "__main__":
    test_binom_small()
    test_exponent_examples()
    test_S_rejects_n_below_two()
    test_S_prefix_issue_354()
    print("ok - S(n)")
