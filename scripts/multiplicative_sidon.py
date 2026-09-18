#!/usr/bin/env python3
"""F(n) for Erdős problem 425 (issue #300).

F(n) is the maximum size of A ⊆ {1,…,n} such that the products ab for
a < b in A are all distinct (a multiplicative Sidon / B₂* set).
"""
from __future__ import annotations


def is_multiplicative_sidon(A: list[int]) -> bool:
    products: set[int] = set()
    for i, a in enumerate(A):
        for b in A[i + 1 :]:
            p = a * b
            if p in products:
                return False
            products.add(p)
    return True


def F(n: int) -> int:
    """Exact F(n) by branch-and-bound (tractable for moderate n)."""
    if n < 1:
        raise ValueError("n must be positive")
    best = 0
    chosen: list[int] = []
    products: set[int] = set()
    nums = list(range(n, 0, -1))

    def ok_add(x: int) -> list[int] | None:
        new_prods = []
        for y in chosen:
            p = x * y
            if p in products:
                return None
            new_prods.append(p)
        return new_prods

    def dfs(i: int) -> None:
        nonlocal best
        if len(chosen) + (len(nums) - i) <= best:
            return
        if i == len(nums):
            best = max(best, len(chosen))
            return
        x = nums[i]
        new_prods = ok_add(x)
        if new_prods is not None:
            chosen.append(x)
            for p in new_prods:
                products.add(p)
            dfs(i + 1)
            for p in new_prods:
                products.remove(p)
            chosen.pop()
        dfs(i + 1)

    dfs(0)
    return best


# Independently recomputed; agrees with the MILP table in issue #300 for n ≤ 24.
KNOWN = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5, 7: 6, 8: 6, 9: 7, 10: 7,
    11: 8, 12: 9, 13: 10, 14: 10, 15: 10, 16: 11, 17: 12, 18: 12,
    19: 13, 20: 13, 21: 13, 22: 14, 23: 15, 24: 15,
}


if __name__ == "__main__":
    import sys
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    for n in range(1, maxn + 1):
        print(n, F(n))
