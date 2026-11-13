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


def _find(k: int, numer: int, denom: int, start: int) -> list[int] | None:
    """One way to write numer/denom as k distinct unit fractions, all >= start."""
    g = gcd(numer, denom)
    numer //= g
    denom //= g
    if numer <= 0 or _harmonic_short(k, numer, denom, start):
        return None
    if k == 1:
        return [denom] if numer == 1 and denom >= start else None
    lo = max(start, (denom + numer - 1) // numer)
    if k == 2:
        hi = (2 * denom) // numer
        for a in range(lo, hi):
            den = numer * a - denom
            if den > 0 and (denom * a) % den == 0:
                b = (denom * a) // den
                if b > a:
                    return [a, b]
        return None
    hi = (k * denom) // numer
    for a in range(lo, hi + 1):
        nn = numer * a - denom
        if nn <= 0:
            continue
        rest = _find(k - 1, nn, denom * a, a + 1)
        if rest is not None:
            return [a, *rest]
    return None


def _find_budget(k: int, numer: int, denom: int, start: int, budget: int) -> list[int] | None:
    """Like _find, but the denominators stay within `budget` of the greedy choice.

    The final two-term split is refused when its search interval is huge, so a
    missed witness is reported as absent rather than scanned indefinitely.
    """
    g = gcd(numer, denom)
    numer //= g
    denom //= g
    if numer <= 0:
        return None
    if k == 1:
        return [denom] if numer == 1 and denom >= start else None
    lo = max(start, (denom + numer - 1) // numer)
    if k == 2:
        hi = (2 * denom) // numer
        if hi - lo > 2_000_000:
            return None
        for a in range(lo, hi):
            den = numer * a - denom
            if den > 0 and (denom * a) % den == 0:
                b = (denom * a) // den
                if b > a:
                    return [a, b]
        return None
    limit = min(lo + budget, (k * denom) // numer)
    for a in range(lo, limit + 1):
        nn = numer * a - denom
        if nn <= 0:
            continue
        rest = _find_budget(k - 1, nn, denom * a, a + 1, budget - (a - lo))
        if rest is not None:
            return [a, *rest]
    return None


def witness_near_greedy(n1: int, k: int, max_budget: int = 3) -> tuple[int, ...] | None:
    """A k-term decomposition starting at n1, if one stays close to greedy."""
    for budget in range(max_budget + 1):
        rest = _find_budget(k - 1, n1 - 1, n1, n1 + 1, budget)
        if rest is not None:
            return (n1, *rest)
    return None


def _exists(k: int, numer: int, denom: int, start: int) -> bool:
    return _find(k, numer, denom, start) is not None


def decomposition(k: int) -> tuple[int, ...]:
    """One increasing k-term Egyptian fraction of 1 whose first term is f(k)."""
    n1 = f(k)
    rest = _find(k - 1, n1 - 1, n1, n1 + 1)
    if rest is None:
        raise RuntimeError(f"missing witness for f({k})")
    return (n1, *rest)


def split_largest(dens: tuple[int, ...]) -> tuple[int, ...]:
    """Replace 1/m by 1/(m+1) + 1/(m(m+1)) for the largest denominator m."""
    largest = max(dens)
    left = largest + 1
    right = largest * (largest + 1)
    if left in dens or right in dens:
        raise ValueError("split collides with an existing denominator")
    return tuple(sorted((*[value for value in dens if value != largest], left, right)))


def sums_to_one(dens: tuple[int, ...]) -> bool:
    if list(dens) != sorted(dens) or len(set(dens)) != len(dens):
        return False
    numer, denom = 0, 1
    for value in dens:
        numer = numer * value + denom
        denom *= value
        g = gcd(numer, denom)
        numer //= g
        denom //= g
    return numer == denom


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


# Issue #271 through k = 21. k = 22 is checked by splitting, and k = 23, 24
# by witness_near_greedy. The posted table ends at k = 24.
ISSUE_PREFIX = {
    3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 5, 11: 6, 12: 6,
    13: 7, 14: 7, 15: 8, 16: 8, 17: 9, 18: 9, 19: 10, 20: 10, 21: 11,
}
