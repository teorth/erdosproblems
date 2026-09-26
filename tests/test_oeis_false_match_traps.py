#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oeis_false_match_traps import partner_divisors, r_pairs


def test_pairs_agree_until_60():
    for n in range(1, 60):
        assert r_pairs(n) == partner_divisors(n), n


def test_first_split_at_60():
    # Issue #356: r(60)=13 (pairs) vs A174903(60)=9 (divisors with a partner).
    assert r_pairs(60) == 13
    assert partner_divisors(60) == 9


def test_a386820_at_15_is_nine():
    # Issue #356 trap 2: A386820 (no minimality) is 9 at n=15; problem 319 is 8.
    from oeis_false_match_traps import a386820
    assert a386820(15) == 9


def test_empty_vs_nonempty_offset():
    from oeis_false_match_traps import empty_vs_nonempty_prefix
    inclusive, nonempty = empty_vs_nonempty_prefix()
    assert inclusive == [2, 3, 5, 8, 14]
    assert nonempty == [0, 1, 2, 4, 7, 13]
    assert [a - b for a, b in zip(inclusive, nonempty[1:])] == [1, 1, 1, 1, 1]


def test_sigma_3328_is_gcd_trap():
    # Issue #356 comment: A241646 vs problem 824. m=3328 has overall gcd 1
    # but no coprime pair in the preimage.
    from math import gcd
    from oeis_false_match_traps import has_coprime_pair, overall_gcd, sigma_preimage
    xs = sigma_preimage(3328)
    assert xs == [1953, 2163, 3193]
    assert overall_gcd(xs) == 1
    assert has_coprime_pair(xs) is False
    assert gcd(1953, 2163) == 21
    assert gcd(1953, 3193) == 31
    assert gcd(2163, 3193) == 103


if __name__ == "__main__":
    test_pairs_agree_until_60()
    test_first_split_at_60()
    test_a386820_at_15_is_nine()
    test_empty_vs_nonempty_offset()
    test_sigma_3328_is_gcd_trap()
    print("ok - oeis false-match traps")
