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


def f(N: int) -> int:
    if N < 1:
        raise ValueError("N >= 1")
    best = 0
    chosen: list[int] = []
    nums = list(range(N, 0, -1))

    def dfs(i: int) -> None:
        nonlocal best
        if len(chosen) + (len(nums) - i) <= best:
            return
        if i == len(nums):
            best = max(best, len(chosen))
            return
        x = nums[i]
        chosen.append(x)
        if is_triple_free(chosen):
            dfs(i + 1)
        chosen.pop()
        dfs(i + 1)

    dfs(0)
    return best


# Issue #354 table for N = 1..30 (exhaustive check here through 20; 21..30 pinned from issue)
ISSUE_PREFIX = [
    1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10, 11, 12, 12, 13, 14, 15, 16, 16,
    17, 18, 19, 19, 20, 21, 22, 23, 24, 24,
]


if __name__ == "__main__":
    import sys
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print([f(n) for n in range(1, maxn + 1)])
