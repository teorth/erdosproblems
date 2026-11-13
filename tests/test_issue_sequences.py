"""Checked ranges from open Erdős-problem issues.

Covering counts are exhaustive through seven moduli. The named reciprocal
maximizers through seventeen moduli are checked directly. e(n), g_k(n), and
v(k) are recomputed on the prefix the search finishes quickly.
"""
import sys
from functools import reduce
from math import lcm
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from irreducible_coverings import is_irreducible_covering, modulus_sets, summary
from multiplicative_sidon import F
from product_representations import g
from rainbow_c4 import e
from vk_unit_fractions import v


def test_issue_509_small_covering_counts():
    # Issue #509: I(k) starts 0,0,0,0,1,4,15 and the extremal rows match.
    for k in range(1, 5):
        assert modulus_sets(k, 12) == []
    five = summary(modulus_sets(5, 12))
    six = summary(modulus_sets(6, 24))
    seven = summary(modulus_sets(7, 48))
    assert (five["count"], five["min_lcm"], five["max_lcm"]) == (1, 12, 12)
    assert abs(five["max_reciprocal"] - 4 / 3) < 1e-9
    assert five["max_set"] == (2, 3, 4, 6, 12)
    assert (six["count"], six["min_lcm"], six["max_lcm"]) == (4, 24, 24)
    assert abs(six["max_reciprocal"] - 17 / 12) < 1e-9
    assert six["max_set"] == (2, 3, 4, 6, 8, 24)
    assert (seven["count"], seven["min_lcm"], seven["max_lcm"]) == (15, 36, 48)
    assert abs(seven["max_reciprocal"] - 35 / 24) < 1e-9
    assert seven["max_set"] == (2, 3, 4, 6, 8, 16, 48)


def test_issue_509_witnesses_are_irreducible_coverings():
    # Modulus sets named in issue #509, with the reciprocal sum from that table.
    rows = {
        (2, 3, 4, 6, 12): "4/3",
        (2, 3, 4, 6, 8, 24): "17/12",
        (2, 3, 4, 6, 8, 16, 48): "35/24",
        (2, 3, 4, 6, 8, 9, 18, 72): "14/9",
        (2, 3, 4, 5, 6, 10, 15, 20, 30): "17/10",
        (2, 3, 4, 5, 6, 8, 10, 15, 20, 40): "109/60",
        (2, 3, 4, 5, 6, 8, 10, 15, 16, 20, 80): "28/15",
        (2, 3, 4, 5, 6, 8, 9, 10, 15, 18, 20, 360): "353/180",
        (2, 3, 4, 5, 6, 8, 9, 10, 15, 16, 18, 20, 720): "91/45",
        (2, 3, 4, 5, 6, 8, 9, 10, 15, 16, 18, 20, 32, 1440): "739/360",
        (2, 3, 4, 5, 6, 8, 9, 10, 15, 16, 18, 20, 27, 54, 2160): "2243/1080",
        (2, 3, 4, 5, 6, 7, 8, 10, 14, 15, 20, 21, 28, 35, 42, 56): "907/420",
        (2, 3, 4, 5, 6, 7, 8, 10, 14, 15, 16, 20, 21, 28, 35, 42, 112): "1859/840",
    }
    for moduli, fraction in rows.items():
        assert is_irreducible_covering(moduli)
        num, den = fraction.split("/")
        total = sum(reduce(lcm, moduli) // n for n in moduli)
        assert total * int(den) == int(num) * reduce(lcm, moduli)


def test_issue_499_exact_edge_counts_through_n_5():
    # Issue #499: e(1)..e(13) starts 0, 1, 3, 5, 7.
    assert [e(n) for n in range(1, 6)] == [0, 1, 3, 5, 7]


def test_issue_444_g2_matches_multiplicative_sidon_and_g3_prefix():
    # g_2 is F from problem 425. g_3 and g_4 are the start of the issue #444 tables.
    for n in range(1, 13):
        assert g(2, n) == F(n)
    assert [g(3, n) for n in range(1, 25)] == [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 12, 13, 14, 15, 16, 16, 17, 17, 18, 19, 20, 21,
    ]
    assert [g(4, n) for n in range(1, 21)] == [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 19,
    ]


def test_issue_403_unit_fraction_denominators_through_k_5():
    # Issue #403, independently recomputed: v(1)..v(5) = 2, 2, 4, 11, 17.
    assert [v(k) for k in range(1, 6)] == [2, 2, 4, 11, 17]
