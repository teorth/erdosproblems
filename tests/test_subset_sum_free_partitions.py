#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from subset_sum_free_partitions import ISSUE_PREFIX, can_subset_sum, f, feasible


def test_subset_sum():
    assert can_subset_sum([1, 2, 4], 7)
    assert can_subset_sum([3, 5], 3)
    assert not can_subset_sum([1, 2], 4)
    assert not can_subset_sum([], 1)


def test_small_n():
    assert f(2) == 1
    assert f(3) == 2
    assert f(11) == 2
    assert f(12) == 3


def test_prefix():
    # Cross-check against the issue #354 table for n <= 14 (fast enough for CI).
    for n, want in enumerate(ISSUE_PREFIX[:13], 2):
        assert f(n) == want, (n, f(n), want)


def test_feasible_bounds():
    assert feasible(12, 3)
    assert not feasible(12, 2)


if __name__ == "__main__":
    test_subset_sum()
    test_small_n()
    test_prefix()
    test_feasible_bounds()
    print("ok - subset-sum-free partitions")
