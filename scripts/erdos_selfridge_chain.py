#!/usr/bin/env python3
"""Erdős–Selfridge descending chain for problem 430 (issue #354).

For integer n, a_1 = n-1 and each later a_k is the greatest integer in
[1, a_{k-1}) whose prime factors are all > n - a_k.
"""
from __future__ import annotations


def prime_factors(n: int) -> set[int]:
    fac: set[int] = set()
    x = n
    while x % 2 == 0:
        fac.add(2)
        x //= 2
    f = 3
    while f * f <= x:
        while x % f == 0:
            fac.add(f)
            x //= f
        f += 2
    if x > 1:
        fac.add(x)
    return fac


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def admissible(a: int, n: int) -> bool:
    """True iff every prime factor of a is > n - a."""
    if a < 2:
        return False
    return all(p > n - a for p in prime_factors(a))


def chain(n: int) -> list[int]:
    """Return the descending chain for problem 430 starting at n-1."""
    if n < 2:
        raise ValueError("n must be at least 2")
    seq = [n - 1]
    while True:
        prev = seq[-1]
        found = None
        for a in range(prev - 1, 0, -1):
            if admissible(a, n):
                found = a
                break
        if found is None:
            break
        seq.append(found)
    return seq


def chain_length(n: int) -> int:
    return len(chain(n))


def all_terms_prime(n: int) -> bool:
    return all(is_prime(a) for a in chain(n))


# Issue #354: chain lengths for n = 3..80
ISSUE_LENGTHS = [
    1, 1, 2, 1, 2, 2, 3, 2, 3, 2, 3, 2, 3, 3, 4, 3, 4, 4, 5, 4, 5, 4, 5, 4, 5, 5, 6, 4, 5, 5,
    6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 6, 7, 6, 7, 6, 7, 7, 8, 8, 9, 8, 9, 8, 9, 8, 9, 7, 8, 7,
    8, 8, 9, 8, 9, 9, 10, 9, 10, 9, 10, 9, 10, 10, 11, 10, 11, 11,
]

# Issue #354: n <= 80 for which every term of the chain is prime
ISSUE_ALL_PRIME = [3, 4, 6, 8, 12, 14, 18, 20, 24, 30, 32, 42, 44, 48, 60, 62, 72, 74]


if __name__ == "__main__":
    import sys

    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for n in range(3, maxn + 1):
        c = chain(n)
        print(f"{n}: len={len(c)} all_prime={all(is_prime(a) for a in c)} {c}")
