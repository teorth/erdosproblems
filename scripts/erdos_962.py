#!/usr/bin/env python3
"""Minimal m(k) for Erdős problem 962 (issue #145).

m(k) is the least m such that every integer in {m+1, …, m+k} has a prime
factor > k.  Equivalently A327909(k) = m(k) + 1 is the start of the run.
"""
from __future__ import annotations


def largest_prime_factor(n: int) -> int:
    if n <= 1:
        return 1
    last = 1
    while n % 2 == 0:
        last = 2
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            last = f
            n //= f
        f += 2
    if n > 1:
        last = n
    return last


def m(k: int, start: int = 0) -> int:
    if k < 1:
        raise ValueError("k must be positive")
    m_cur = max(start, 0)
    while True:
        blocked = False
        for j in range(m_cur + 1, m_cur + k + 1):
            if largest_prime_factor(j) <= k:
                m_cur = j
                blocked = True
                break
        if not blocked:
            return m_cur


def a327909(k: int) -> int:
    """OEIS A327909: start of a run of k integers each with a prime factor > k."""
    return m(k) + 1


# OEIS A327909 prefix (n = 1..30)
A327909_PREFIX = [
    2, 5, 13, 19, 55, 65, 113, 151, 151, 226, 364, 406, 736, 736, 1057, 1057,
    1409, 1409, 2059, 2059, 2313, 2313, 2313, 2313, 2313, 2313, 2313, 6007, 6961, 6961,
]


def sequence_m(maxn: int = 20) -> list[int]:
    out = []
    prev = 0
    for k in range(1, maxn + 1):
        prev = m(k, start=prev)
        out.append(prev)
    return out


if __name__ == "__main__":
    import sys
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for k in range(1, maxn + 1):
        print(k, m(k), a327909(k))
