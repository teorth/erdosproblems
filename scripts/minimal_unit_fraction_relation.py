#!/usr/bin/env python3
"""Largest minimal signed subset for Erdős problem 319 (issue #354).

The size of the largest A ⊆ {1..N} with a signing δ: A → {-1, 1} such that
the signed sum of 1/n over A is 0, and the same signing has nonzero signed
sum on every nonempty proper subset.
"""
from __future__ import annotations

from itertools import combinations
from math import lcm


def _subset_sums(weights: list[int]) -> set[int]:
    sums = {0}
    for weight in weights:
        sums |= {total + weight for total in sums}
    return sums


def has_minimal_signing(values: tuple[int, ...]) -> bool:
    if not values:
        return False
    span = 1
    for value in values:
        span = lcm(span, value)
    weights = [span // value for value in values]
    total = sum(weights)
    if total % 2:
        return False
    target = total // 2
    count = len(weights)

    def partitions(index: int, acc: int, chosen: list[int]) -> bool:
        if acc == target:
            if not chosen or len(chosen) == count:
                return False
            positive = [weights[j] for j in chosen]
            negative = [weights[j] for j in range(count) if j not in chosen]
            if _subset_sums(positive) & _subset_sums(negative) == {0, target}:
                return True
            return False
        if index == count or acc > target:
            return False
        chosen.append(index)
        if partitions(index + 1, acc + weights[index], chosen):
            return True
        chosen.pop()
        return partitions(index + 1, acc, chosen)

    return partitions(0, 0, [])


def largest(N: int) -> int:
    """Largest admissible |A| inside {1..N}. Zero when no such A exists."""
    if N < 1:
        raise ValueError("N must be positive")
    for size in range(N, 0, -1):
        for subset in combinations(range(1, N + 1), size):
            if has_minimal_signing(subset):
                return size
    return 0


# Issue #354, N = 1..19.
ISSUE_PREFIX = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 6, 6, 6, 8, 8, 8, 10, 10]
