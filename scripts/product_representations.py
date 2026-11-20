#!/usr/bin/env python3
"""g_k(n) for Erdős problem 796 (issue #444).

g_k(n) is the largest A subset of {1..n} such that every positive integer has
fewer than k representations as a product of two distinct elements of A.
g_2 is the multiplicative Sidon function.
"""
from __future__ import annotations


def g(k: int, n: int) -> int:
    if k < 2:
        raise ValueError("k must be at least 2")
    if n < 1:
        raise ValueError("n must be positive")
    nums = list(range(n, 0, -1))
    best = 0
    chosen: list[int] = []
    counts: dict[int, int] = {}

    def can_add(value: int) -> list[int] | None:
        touched = []
        for other in chosen:
            product = value * other
            if counts.get(product, 0) + 1 >= k:
                return None
            touched.append(product)
        return touched

    def search(index: int) -> None:
        nonlocal best
        if len(chosen) + (len(nums) - index) <= best:
            return
        if index == len(nums):
            best = max(best, len(chosen))
            return
        value = nums[index]
        touched = can_add(value)
        if touched is not None:
            chosen.append(value)
            for product in touched:
                counts[product] = counts.get(product, 0) + 1
            search(index + 1)
            for product in touched:
                counts[product] -= 1
                if counts[product] == 0:
                    del counts[product]
            chosen.pop()
        search(index + 1)

    search(0)
    return best
