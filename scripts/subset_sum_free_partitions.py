#!/usr/bin/env python3
"""f(n) for Erdős problem 360 (issue #354): min classes in a partition of
{1,...,n-1} so that n is not a subset-sum of any single class."""
from __future__ import annotations


def can_subset_sum(nums: list[int], target: int) -> bool:
    """True if some nonempty subset of nums sums to target."""
    reachable = {0}
    for x in nums:
        reachable |= {s + x for s in reachable if s + x <= target}
        if target in reachable:
            return True
    return False


def feasible(n: int, k: int) -> bool:
    """Whether {1,...,n-1} can be colored with k colors so no color class
    has a subset summing to n."""
    elems = list(range(1, n))

    def search(i: int, classes: list[list[int]]) -> bool:
        if i == len(elems):
            return True
        x = elems[i]
        for c in classes:
            c.append(x)
            if not can_subset_sum(c, n) and search(i + 1, classes):
                return True
            c.pop()
        return False

    return search(0, [[] for _ in range(k)])


def f(n: int) -> int:
    """Minimal number of classes for problem 360."""
    if n < 2:
        raise ValueError("n must be at least 2")
    k = 1
    while True:
        if feasible(n, k):
            return k
        k += 1


# Values from issue #354 for n = 2..26
ISSUE_PREFIX = [
    1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
]


if __name__ == "__main__":
    import sys

    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print([f(n) for n in range(2, maxn + 1)])
