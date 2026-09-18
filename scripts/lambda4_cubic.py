#!/usr/bin/env python3
"""Mercer's cubic for lambda(4), Erdős problem 510 / issue #392.

lambda(4) is claimed to be the unique real root of
512 y^3 - 1227 y^2 + 600 y + 125 = 0, about 1.5195578816428.
"""
from __future__ import annotations


def cubic(y: float) -> float:
    return ((512 * y - 1227) * y + 600) * y + 125


def has_sign_change(lo: float, hi: float) -> bool:
    return cubic(lo) * cubic(hi) < 0


def unique_real_root(lo: float = 1.1, hi: float = 1.6, steps: int = 80) -> float:
    """Bisection on an interval where the cubic changes sign once."""
    flo, fhi = cubic(lo), cubic(hi)
    if not has_sign_change(lo, hi):
        raise ValueError("no sign change")
    for _ in range(steps):
        mid = (lo + hi) / 2
        if cubic(mid) * flo <= 0:
            hi = mid
            fhi = cubic(mid)
        else:
            lo = mid
            flo = cubic(mid)
    return (lo + hi) / 2


def derivative(y: float) -> float:
    return (3 * 512 * y - 2 * 1227) * y + 600
