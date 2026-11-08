"""Checked prefixes of the tables in open Erdős-problem issues.

The full ranges in those issues are large. These tests recompute the range
that is exact by the search in this repository, and check the explicit
covering-system witnesses from issue #509 directly.
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
    # g_2 is F from problem 425. The g_3 prefix is the start of issue #444.
    for n in range(1, 13):
        assert g(2, n) == F(n)
    assert [g(3, n) for n in range(1, 13)] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11]


def test_issue_403_unit_fraction_denominators_through_k_5():
    # Issue #403, independently recomputed: v(1)..v(5) = 2, 2, 4, 11, 17.
    assert [v(k) for k in range(1, 6)] == [2, 2, 4, 11, 17]
