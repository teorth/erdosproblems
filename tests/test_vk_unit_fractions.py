#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from vk_unit_fractions import appearing_denominators, decompositions, v


def test_k1_no_decomposition_above_one():
    # Only 1 = 1/1, so every m > 1 is absent.
    assert decompositions(1, 5) == [(1,)]
    assert v(1) == 2


def test_k2_no_strictly_increasing_split():
    assert decompositions(2, 10) == []
    assert v(2) == 2


def test_k3_uses_2_3_6_and_misses_4():
    triples = decompositions(3, 12)
    assert (2, 3, 6) in triples
    dens = appearing_denominators(3, 12)
    assert 2 in dens and 3 in dens and 6 in dens
    assert 4 not in dens
    assert v(3) == 4


def test_k4_matches_issue_403():
    # ncap must be large enough that 7,8,9,10 appear (else v would look like 7).
    assert v(4, ncap=80) == 11
    dens = appearing_denominators(4, 80)
    for m in range(2, 11):
        assert m in dens, m
    assert 11 not in dens


def test_rejects_nonpositive_k():
    try:
        v(0)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    test_k1_no_decomposition_above_one()
    test_k2_no_strictly_increasing_split()
    test_k3_uses_2_3_6_and_misses_4()
    test_k4_matches_issue_403()
    test_rejects_nonpositive_k()
    print("ok - v(k)")
