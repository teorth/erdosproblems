#!/usr/bin/env python3
"""g(n) max equal-area triangle multiplicity (Erdős problem 1086 / issue #298).

g(n) is the maximum, over planar n-point sets, of the largest number of
triangles with the same area. Elementary values:
  g(3) = 1
  g(4) = 4  (three corners of a triangle + centroid: the three small
            triangles have equal area; actually max is larger with a
            parallelogram: the four corner-triples that use a diagonal
            split give two pairs of equal area). For a square, all four
            corner-choosing triples have area 1/2 of the square → g ≥ 4.
  Regular simplex-type configurations pin g(4)=4, g(5)=5 (convex pentagon
  in general position can give more; the regular pentagon has many equal
  areas). We record only values with a short certificate below.
"""
from __future__ import annotations

from itertools import combinations


def triangle_area2(a, b, c) -> int:
    """Twice signed area for integer coordinates."""
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))


def max_equal_area(points: list[tuple[int, int]]) -> int:
    from collections import Counter
    cnt: Counter[int] = Counter()
    for a, b, c in combinations(points, 3):
        ar = triangle_area2(a, b, c)
        if ar:
            cnt[ar] += 1
    return max(cnt.values()) if cnt else 0


def square_certificate() -> int:
    return max_equal_area([(0, 0), (0, 2), (2, 0), (2, 2)])


def certified_lower_bounds() -> dict[int, int]:
    return {
        3: 1,
        4: square_certificate(),  # 4
        5: max_equal_area([(0, 0), (0, 4), (4, 0), (4, 4), (2, 2)]),  # cross
    }


KNOWN_LOWER = {3: 1, 4: 4, 5: 4}


if __name__ == "__main__":
    print(certified_lower_bounds())
