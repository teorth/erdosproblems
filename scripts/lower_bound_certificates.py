#!/usr/bin/env python3
"""Certificates from issue #473.

Problem 30: a finite Sidon set A ⊆ {1..N} (every sum a + b with a <= b is
unique) is a lower bound on the largest Sidon subset of that interval.

Problem 20: a k-uniform family with no 3-petal sunflower has size one less
than a lower bound for the number of sets that forces a 3-sunflower.
"""
from __future__ import annotations

from itertools import combinations


# (N, set). Sizes 12, 17, 22, 28 are the lower bounds stated in the issue.
SIDON_SETS = {
    100: (1, 4, 14, 15, 20, 35, 53, 61, 65, 88, 90, 97),
    250: (4, 11, 23, 25, 29, 49, 90, 140, 143, 153, 170, 175, 186, 209, 217, 245, 246),
    500: (8, 24, 32, 33, 111, 126, 164, 166, 184, 285, 292, 314, 353, 374, 380, 384, 397, 430, 449, 460, 494, 497),
    1000: (7, 10, 57, 72, 132, 231, 236, 240, 265, 285, 349, 367, 377, 446, 537, 572, 615, 631, 657, 773, 797, 804, 871, 927, 948, 959, 960, 1000),
}

SUNFLOWER_FREE = {
    (3, 9): (
        (1, 7, 9), (3, 5, 6), (1, 6, 8), (2, 5, 9), (2, 3, 9), (4, 7, 8), (1, 4, 9),
        (2, 3, 6), (4, 7, 9), (1, 4, 8), (6, 7, 8), (3, 5, 9), (2, 5, 6), (1, 6, 7),
    ),
    (4, 11): (
        (1, 5, 9, 10), (1, 3, 7, 11), (2, 5, 6, 7), (5, 7, 8, 11), (7, 8, 10, 11),
        (2, 4, 10, 11), (1, 3, 6, 7), (5, 8, 10, 11), (3, 5, 9, 10), (1, 3, 6, 8),
        (2, 3, 7, 8), (1, 6, 7, 11), (2, 4, 5, 11), (4, 5, 6, 8), (5, 7, 8, 10),
        (1, 4, 8, 10), (4, 5, 6, 7), (4, 5, 9, 11), (3, 6, 7, 11), (2, 4, 9, 10),
        (2, 9, 10, 11), (3, 6, 8, 11), (2, 5, 9, 11), (2, 3, 7, 10), (2, 4, 6, 9),
        (4, 9, 10, 11), (1, 3, 8, 11), (1, 6, 8, 11), (2, 5, 6, 8), (5, 7, 10, 11),
    ),
}


def is_sidon(values: tuple[int, ...], limit: int) -> bool:
    if len(values) != len(set(values)) or not values:
        return False
    if min(values) < 1 or max(values) > limit:
        return False
    sums = [a + b for i, a in enumerate(values) for b in values[i:]]
    return len(sums) == len(set(sums))


def is_sunflower_free(family: tuple[tuple[int, ...], ...], k: int, universe: int) -> bool:
    sets = [frozenset(block) for block in family]
    if len(sets) != len(set(sets)):
        return False
    for block in sets:
        if len(block) != k or min(block) < 1 or max(block) > universe:
            return False
    for a, b, c in combinations(sets, 3):
        if a & b == a & c == b & c:
            return False
    return True
