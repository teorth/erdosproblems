#!/usr/bin/env python3
"""f(N) for Erdős problem 536 (issue #354).

Maximum size of A ⊆ {1,…,N} with no three distinct a,b,c ∈ A satisfying
lcm(a,b)=lcm(b,c)=lcm(a,c).
"""
from __future__ import annotations

import math
from itertools import combinations


def lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


def is_triple_free(A: list[int]) -> bool:
    for a, b, c in combinations(A, 3):
        x = lcm(a, b)
        if x == lcm(b, c) == lcm(a, c):
            return False
    return True


def _bad_triples(N: int) -> list[tuple[int, int, int]]:
    bad = []
    for a, b, c in combinations(range(1, N + 1), 3):
        ab = lcm(a, b)
        if ab == lcm(a, c) == lcm(b, c):
            bad.append((a, b, c))
    return bad


def _min_deletions(triples: list[tuple[int, int, int]]) -> int:
    """Smallest set that meets every triple. The complement is a maximum triple-free set."""
    best = len({v for triple in triples for v in triple}) + 1

    def search(index: int, deleted: set[int]) -> None:
        nonlocal best
        if len(deleted) >= best:
            return
        while index < len(triples):
            a, b, c = triples[index]
            if a in deleted or b in deleted or c in deleted:
                index += 1
                continue
            break
        else:
            best = len(deleted)
            return
        a, b, c = triples[index]
        for value in (a, b, c):
            deleted.add(value)
            search(index + 1, deleted)
            deleted.remove(value)

    search(0, set())
    return best


def f(N: int) -> int:
    if N < 1:
        raise ValueError("N >= 1")
    triples = _bad_triples(N)
    if not triples:
        return N
    return N - _min_deletions(triples)


# Issue #354 table for N = 1..45.
ISSUE_PREFIX = [
    1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10, 11, 12, 12, 13, 14, 15, 16, 16, 17, 18, 19, 19, 20,
    21, 22, 23, 24, 24, 25, 26, 27, 28, 28, 29, 30, 31, 32, 32, 33, 33, 34, 35, 35,
]


if __name__ == "__main__":
    import sys
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print([f(n) for n in range(1, maxn + 1)])
