#!/usr/bin/env python3
"""v(k) for Erdős problem 293 (issue #403).

v(k) is the smallest integer m > 1 that does not occur as a denominator in any
strictly increasing k-term unit-fraction decomposition of 1.
"""
from __future__ import annotations

from math import gcd


def decompositions(k: int, ncap: int) -> list[tuple[int, ...]]:
    """All 1 = 1/n_1 + … + 1/n_k with 1 ≤ n_1 < … < n_k ≤ ncap."""
    out: list[tuple[int, ...]] = []

    def rec(k_left: int, numer: int, denom: int, start: int, acc: list[int]) -> None:
        if k_left == 1:
            if numer == 1 and denom >= start and denom <= ncap:
                out.append(tuple(acc + [denom]))
            return
        lo = max(start, (denom + numer - 1) // numer)
        hi = min(ncap, k_left * denom // numer)
        for n in range(lo, hi + 1):
            nn = numer * n - denom
            nd = denom * n
            if nn <= 0:
                continue
            g = gcd(nn, nd)
            rec(k_left - 1, nn // g, nd // g, n + 1, acc + [n])

    rec(k, 1, 1, 1, [])
    return out


def appearing_denominators(k: int, ncap: int) -> set[int]:
    dens: set[int] = set()
    for t in decompositions(k, ncap):
        dens.update(t)
    return dens


def v(k: int, ncap: int | None = None) -> int:
    """Smallest m > 1 absent from all k-term decompositions with n_k ≤ ncap."""
    if k < 1:
        raise ValueError("k must be positive")
    if ncap is not None and ncap < 1:
        raise ValueError("ncap must be positive")
    if ncap is None:
        ncap = {1: 2, 2: 2, 3: 12, 4: 80, 5: 200}[k]
    dens = appearing_denominators(k, ncap)
    m = 2
    while m in dens:
        m += 1
        if m > ncap + 1:
            raise RuntimeError(f"v({k}) not found below {ncap}")
    return m
