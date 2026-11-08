#!/usr/bin/env python3
"""f(k) for Erdős problem 284 (issue #271).

f(k) is the largest n_1 such that 1 = 1/n_1 + ... + 1/n_k for some
integers n_1 < n_2 < ... < n_k. f(2) does not exist.
"""
from __future__ import annotations

from math import gcd


def _harmonic_short(k: int, numer: int, denom: int, start: int) -> bool:
    """True when the k shortest unit fractions from start sum to less than numer/denom."""
    if k <= 0:
        return numer > 0
    left_n, left_d = 0, 1
    for offset in range(k):
        piece = start + offset
        left_n = left_n * piece + left_d
        left_d *= piece
        g = gcd(left_n, left_d)
        left_n //= g
        left_d //= g
    return left_n * denom < numer * left_d


def _exists(k: int, numer: int, denom: int, start: int) -> bool:
    """Whether numer/denom is a sum of k distinct unit fractions, all >= start."""
    g = gcd(numer, denom)
    numer //= g
    denom //= g
    if numer <= 0:
        return False
    if _harmonic_short(k, numer, denom, start):
        return False
    if k == 1:
        return numer == 1 and denom >= start
    lo = max(start, (denom + numer - 1) // numer)
    if k == 2:
        hi = (2 * denom) // numer
        for a in range(lo, hi):
            den = numer * a - denom
            if den > 0 and (denom * a) % den == 0:
                b = (denom * a) // den
                if b > a:
                    return True
        return False
    hi = (k * denom) // numer
    for a in range(lo, hi + 1):
        nn = numer * a - denom
        if nn <= 0:
            continue
        if _exists(k - 1, nn, denom * a, a + 1):
            return True
    return False


def f(k: int) -> int:
    """Largest first denominator in a k-term Egyptian fraction of 1."""
    if k < 3:
        raise ValueError("k must be at least 3")
    hi = k
    while hi >= 2 and _harmonic_short(k - 1, hi - 1, hi, hi + 1):
        hi -= 1
    while hi >= 2:
        if _exists(k - 1, hi - 1, hi, hi + 1):
            return hi
        hi -= 1
    raise RuntimeError(f"no {k}-term decomposition")


# Issue #271, recomputed here for k = 3..21. k = 22..24 is left out.
ISSUE_PREFIX = {
    3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 5, 11: 6, 12: 6,
    13: 7, 14: 7, 15: 8, 16: 8, 17: 9, 18: 9, 19: 10, 20: 10, 21: 11,
}
