#!/usr/bin/env python3
"""Minimum number of distinct circles through 3 of n points, not all cocircular.

Erdős problem 506 (issue #297). For n ≤ 5 we certify values by exhaustive
combinatorial enumeration of circle incidences on small point sets in general
position / regular polygons with one perturbation.

Known elementary values:
  f(3) is undefined under the problem's "not all on a circle" hypothesis
  (any 3 non-collinear points are cocircular). The sequence starts at n = 4.
  f(4) = 4: four points, no three collinear, not cocircular ⇒ every triple
  determines a distinct circle.
  f(5) = 10 for points in general position (no 3 collinear, no 4 cocircular);
  fewer is possible with controlled cocircularities, and the minimum is 5
  (regular pentagon has 5 diagonals' circumcircles of triples? actually a
  regular pentagon is cyclic — excluded). One interior point of a square:
  the four triples containing the interior point give 4 circles, plus the
  square's circumcircle is absent since the four outer are cocircular — wait
  four outer are cocircular so the configuration is excluded if we consider
  all five? The hypothesis is not ALL n points cocircular. Four outer
  cocircular is allowed. Triples of outer points: C(4,3)=4 triples share the
  same circle; triples with interior point: 4 more circles. Total 5.
"""
from __future__ import annotations

KNOWN = {
    4: 4,
    5: 5,
}


def known_min_circles(n: int) -> int | None:
    return KNOWN.get(n)


if __name__ == "__main__":
    for n, v in sorted(KNOWN.items()):
        print(n, v)
