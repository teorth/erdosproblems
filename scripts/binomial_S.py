#!/usr/bin/env python3
"""S(n) for Erdős problem 379 (issue #354).

S(n) = min_{0 < k < n} max_p v_p(C(n,k)).

Uses Kummer's theorem / digit-sum formula for the p-adic valuation of
binomial coefficients, so S(n) can be computed without building C(n,k).
"""
from __future__ import annotations


def digit_sum(n: int, p: int) -> int:
    s = 0
    while n:
        s += n % p
        n //= p
    return s


def primes_upto(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i : n + 1 : i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i, v in enumerate(sieve) if v]


def valuation_binom(n: int, k: int, p: int) -> int:
    return (digit_sum(k, p) + digit_sum(n - k, p) - digit_sum(n, p)) // (p - 1)


def max_exponent(n: int, k: int) -> int:
    return max(valuation_binom(n, k, p) for p in primes_upto(n))


def S(n: int) -> int:
    if n < 2:
        raise ValueError("S is defined for n >= 2")
    return min(max_exponent(n, k) for k in range(1, n))


# Issue #354 lists S(2)..S(40).
ISSUE_PREFIX = [
    1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1,
    2, 1, 1, 1, 2, 1, 1, 1, 1,
]


if __name__ == "__main__":
    import sys

    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    print([S(n) for n in range(2, maxn + 1)])
