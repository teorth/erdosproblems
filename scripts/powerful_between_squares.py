#!/usr/bin/env python3
"""h(n) for Erdős problem 942 (issue #354): powerful integers in [n²,(n+1)²)."""
from __future__ import annotations


def is_powerful(m: int) -> bool:
    if m <= 0:
        return False
    if m == 1:
        return True
    n = m
    e = 0
    while n % 2 == 0:
        n //= 2
        e += 1
    if e == 1:
        return False
    f = 3
    while f * f <= n:
        e = 0
        while n % f == 0:
            n //= f
            e += 1
        if e == 1:
            return False
        f += 2
    return n == 1


def h(n: int) -> int:
    lo = n * n
    hi = (n + 1) * (n + 1)
    return sum(1 for m in range(lo, hi) if is_powerful(m))


ISSUE_PREFIX = [
    1, 2, 1, 1, 3, 1, 1, 2, 1, 2, 3, 1, 1, 3, 2, 2, 1, 2, 2, 2, 1, 3, 1, 1, 3, 1, 1, 2, 2, 1,
]


if __name__ == "__main__":
    import sys
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print([h(n) for n in range(1, maxn + 1)])
