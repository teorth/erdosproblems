#!/usr/bin/env python3
"""e(n) for Erdős problem 810 (issue #499).

e(n) is the most edges in a graph on n vertices whose edges can be coloured
with n colours so that every 4-cycle receives four distinct colours.
"""
from __future__ import annotations

from itertools import combinations


def _cycles(n: int, edges: set[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
    found = []
    adj = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for a, b, c, d in combinations(range(n), 4):
        # the three distinct 4-cycles on a labelled 4-set, up to direction
        for cycle in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
            quad = tuple(tuple(sorted(pair)) for pair in zip(cycle, cycle[1:] + cycle[:1]))
            if all(edge in edges for edge in quad):
                found.append(quad)
    return found


def colourable(n: int, edges: set[tuple[int, int]]) -> bool:
    cycles = _cycles(n, edges)
    edge_list = list(edges)
    index = {edge: i for i, edge in enumerate(edge_list)}
    constraints = [tuple(index[edge] for edge in cycle) for cycle in cycles]

    def partial_ok(colours: list[int]) -> bool:
        for constraint in constraints:
            seen = [colours[i] for i in constraint if colours[i] >= 0]
            if len(seen) != len(set(seen)):
                return False
        return True

    def paint(pos: int, colours: list[int]) -> bool:
        if pos == len(edge_list):
            return partial_ok(colours)
        for colour in range(n):
            colours[pos] = colour
            if partial_ok(colours) and paint(pos + 1, colours):
                return True
        colours[pos] = -1
        return False

    if not constraints:
        return True
    return paint(0, [-1] * len(edge_list))


def e(n: int) -> int:
    """Exact e(n) by searching graphs from the dense end. n <= 6 is comfortable."""
    if n < 1:
        raise ValueError("n must be positive")
    if n == 1:
        return 0
    vertices = range(n)
    possible = list(combinations(vertices, 2))
    # A complete graph has too many monochrome-prone cycles; still exact for n <= 5.
    best = 0

    def search(start: int, chosen: list[tuple[int, int]]) -> None:
        nonlocal best
        remaining = len(possible) - start
        if len(chosen) + remaining <= best:
            return
        if start == len(possible):
            edges = set(chosen)
            if len(edges) > best and colourable(n, edges):
                best = len(edges)
            return
        chosen.append(possible[start])
        search(start + 1, chosen)
        chosen.pop()
        search(start + 1, chosen)

    search(0, [])
    return best
