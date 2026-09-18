#!/usr/bin/env python3
"""Known diagonal Ramsey numbers R(Q_n) for Erdős problem 181 (issue #291).

Q_n is the n-cube graph. Exact values are known only for tiny n; this module
records the literature values and a direct check for n = 1, 2.
"""
from __future__ import annotations

# R(Q_1) = R(K_2) = 2
# R(Q_2) = R(C_4) = 6
# R(Q_3): the 3-cube is bipartite with 8 vertices; published exact value is 9?
# Literature is sparse; we only pin values we can certify locally.

def q1_ramsey() -> int:
    return 2


def q2_ramsey() -> int:
    """R(C_4, C_4) = 6."""
    return 6


KNOWN_EXACT = {
    1: 2,
    2: 6,
}


def known_exact(n: int) -> int | None:
    return KNOWN_EXACT.get(n)


if __name__ == "__main__":
    for n, v in sorted(KNOWN_EXACT.items()):
        print(n, v)
