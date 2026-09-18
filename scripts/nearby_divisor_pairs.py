#!/usr/bin/env python3
"""r(n) for Erdős problem 449 (reported in issue #354).

r(n) = #{(d1, d2) : d1 | n, d2 | n, d1 < d2 < 2 d1}.
"""
from __future__ import annotations

import math


def divisors(n: int) -> list[int]:
    out = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            out.append(i)
            if i * i != n:
                out.append(n // i)
    return sorted(out)


def r(n: int) -> int:
    ds = divisors(n)
    count = 0
    for i, d1 in enumerate(ds):
        for d2 in ds[i + 1 :]:
            if d2 < 2 * d1:
                count += 1
            else:
                break
    return count


# Issue #354 table for n = 1..90
ISSUE_PREFIX = [
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0, 0, 5, 0, 0, 0, 1, 0, 5,
    0, 0, 0, 0, 1, 6, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 13,
    0, 0, 1, 0, 0, 3, 0, 0, 0, 3, 0, 11, 0, 0, 2, 0, 1, 2, 0, 5, 0, 0, 0, 11, 0, 0, 0, 1, 0, 13,
]


if __name__ == "__main__":
    import sys
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(",".join(str(r(n)) for n in range(1, maxn + 1)))
