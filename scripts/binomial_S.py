#!/usr/bin/env python3
"""S(n) for Erdős problem 379 (issue #354).

S(n) is min_{0<k<n} of the largest exponent in the prime factorization of
binom(n,k). Equivalently: the largest e such that, for every k, some prime
power p^e divides binom(n,k).
"""
from __future__ import annotations

from math import gcd


def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    den = 1
    for i in range(k):
        num *= n - i
        den *= i + 1
        g = gcd(num, den)
        num //= g
        den //= g
    return num // den


def largest_prime_power_exponent(m: int) -> int:
    if m <= 1:
        return 0
    best = 1
    x = m
    p = 2
    while p * p <= x:
        if x % p == 0:
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            if e > best:
                best = e
        p += 1 if p == 2 else 2
    # leftover factor is 1 or a prime, so the exponent is 1
    return best


def S(n: int) -> int:
    if n < 2:
        raise ValueError("S is defined for n >= 2")
    return min(largest_prime_power_exponent(binomial(n, k)) for k in range(1, n))
