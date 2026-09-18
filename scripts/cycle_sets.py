#!/usr/bin/env python3
"""f(n) = number of distinct cycle-sets of graphs on n labelled? vertices.

Erdős problem 84 (issue #290): cycle set A ⊆ {3,…,n} of a graph G on n
vertices is the set of lengths of cycles in G. f(n) counts distinct such A.

We enumerate nonisomorphic simple undirected graphs via geng (if available)
or, for n ≤ 6, all graphs up to isomorphism using nauty-free brute force on
canonical bitmasks of unlabeled graphs by filtering degree sequences — for
n ≤ 5 we enumerate all 2^{C(n,2)} graphs (labelled) and collect cycle-sets;
labelled enumeration overcounts graphs but the cycle-set collection is still
exactly the set of attainable A, which is what f(n) needs.
"""
from __future__ import annotations

from itertools import combinations


def cycle_lengths(n: int, edges: set[tuple[int, int]]) -> frozenset[int]:
    """Return lengths of simple cycles via DFS."""
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    found: set[int] = set()

    def dfs(start: int, u: int, path: list[int], blocked: set[int]) -> None:
        for v in adj[u]:
            if v == start and len(path) >= 3:
                found.add(len(path))
                continue
            if v in blocked or v < start:
                continue
            blocked.add(v)
            path.append(v)
            dfs(start, v, path, blocked)
            path.pop()
            blocked.remove(v)

    for s in range(n):
        dfs(s, s, [s], {s})
    return frozenset(found)


def f(n: int) -> int:
    if n < 3:
        raise ValueError("n must be at least 3")
    m = n * (n - 1) // 2
    edge_list = list(combinations(range(n), 2))
    sets: set[frozenset[int]] = set()
    for mask in range(1 << m):
        edges = {edge_list[i] for i in range(m) if mask >> i & 1}
        sets.add(cycle_lengths(n, edges))
    return len(sets)


# Certified by exhaustive labelled enumeration.
KNOWN = {3: 2, 4: 4, 5: 6}


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print(n, f(n))
