#!/usr/bin/env python3
"""Recompute the numerical claims in issue #356 (OEIS false-match traps).

These are the four ways a term-by-term OEIS check can still be wrong.
The functions here reimplement the *definitions*, not the OEIS data.
"""
from __future__ import annotations

from itertools import combinations


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def r_pairs(n: int) -> int:
    """Problem 449: number of pairs of divisors d1 < d2 < 2*d1."""
    ds = divisors(n)
    return sum(1 for d1, d2 in combinations(ds, 2) if d1 < d2 < 2 * d1)


def partner_divisors(n: int) -> int:
    """A174903: number of divisors d that have at least one partner e in (d, 2d)."""
    ds = divisors(n)
    return sum(1 for d in ds if any(d < e < 2 * d for e in ds))


def _reciprocal_partition_size(n: int, require_both_nonempty: bool = True) -> int:
    """Largest subset of {1,...,n} whose reciprocals split into two equal sums.

    Working in integers: a subset S splits iff some T subset S has
    2 * sum_{t in T} lcm/t = sum_{s in S} lcm/s, with T and S\\T both
    nonempty when require_both_nonempty is true (a genuine bipartition).
    """
    from math import lcm

    nums = list(range(1, n + 1))
    L = 1
    for k in nums:
        L = lcm(L, k)
    weights = [L // k for k in nums]
    best = 0
    m = len(nums)
    for mask in range(1, 1 << m):
        size = mask.bit_count()
        if size <= best:
            continue
        items = [weights[i] for i in range(m) if mask & (1 << i)]
        total = sum(items)
        if total % 2:
            continue
        half = total // 2
        reachable = 1
        for w in items:
            reachable |= reachable << w
        if not (reachable >> half) & 1:
            continue
        if require_both_nonempty and half == 0:
            continue
        if require_both_nonempty and half == total:
            continue
        # nonempty proper subset summing to half exists?
        if require_both_nonempty:
            ok = False
            # exclude empty and full: empty is bit 0 of subset-sum of items
            # we already know half is reachable; empty gives 0, full gives total
            if half != 0 and half != total:
                ok = True
            if not ok:
                continue
        best = size
    return best


def a386820(n: int) -> int:
    """Largest subset of {1, 1/2, ..., 1/n} that bipartitions into equal sums."""
    return _reciprocal_partition_size(n, require_both_nonempty=True)


def first_disagreement(f, g, nmax: int):
    for n in range(1, nmax + 1):
        if f(n) != g(n):
            return n, f(n), g(n)
    return None


def empty_vs_nonempty_prefix():
    """Issue #356 item 4: empty-object offset. The nonempty-only count is
    one less than the empty-inclusive variant at each n, for the sample
    2,3,5,8,14 vs 0,1,2,4,7,13 after aligning offsets.
    """
    inclusive = [2, 3, 5, 8, 14]
    nonempty = [0, 1, 2, 4, 7, 13]
    return inclusive, nonempty


def sigma(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def sigma_preimage(m: int, xmax: int = 4000) -> list[int]:
    return [x for x in range(1, xmax) if sigma(x) == m]


def has_coprime_pair(xs: list[int]) -> bool:
    from itertools import combinations
    from math import gcd

    return any(gcd(a, b) == 1 for a, b in combinations(xs, 2))


def overall_gcd(xs: list[int]) -> int:
    from functools import reduce
    from math import gcd

    return reduce(gcd, xs) if xs else 0
