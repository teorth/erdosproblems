#!/usr/bin/env python3
"""Irreducible covering systems for Erdős problem 1189 (issue #509).

A set of distinct moduli n_1, ..., n_k >= 2 is counted when some choice of
residues makes the congruences cover every integer, and no modulus can be
dropped. I(k) is the number of such modulus sets. The lcm of a set is n_k
in the usual notation, and the table in the issue records min n_k, max n_k,
and the maximum of sum 1/n_i.
"""
from __future__ import annotations

from functools import reduce
from math import lcm


def _irreducible(moduli: tuple[int, ...], residues: tuple[int, ...]) -> bool:
    span = reduce(lcm, moduli)
    owners: list[list[int]] = [[] for _ in range(span)]
    for index, (residue, modulus) in enumerate(zip(residues, moduli)):
        for value in range(residue % modulus, span, modulus):
            owners[value].append(index)
    return all(any(len(owners[value]) == 1 and owners[value][0] == index for value in range(span)) for index in range(len(moduli)))


def is_irreducible_covering(moduli: tuple[int, ...]) -> bool:
    """Whether these moduli are the moduli of an irreducible covering."""
    moduli = tuple(sorted(set(moduli)))
    if len(moduli) != len(set(moduli)) or any(n < 2 for n in moduli):
        return False
    if sum(1 / n for n in moduli) < 1 - 1e-12:
        return False
    span = reduce(lcm, moduli)
    universe = set(range(span))

    def search(remaining: tuple[int, ...], uncovered: set[int], residues: dict[int, int]) -> bool:
        if not remaining:
            got = tuple(residues[i] for i in range(len(moduli)))
            return not uncovered and _irreducible(moduli, got)
        if not uncovered:
            return False
        target = min(uncovered)
        for index in remaining:
            residue = target % moduli[index]
            hit = {value for value in uncovered if value % moduli[index] == residue}
            residues[index] = residue
            rest = tuple(i for i in remaining if i != index)
            if search(rest, uncovered - hit, residues):
                return True
            del residues[index]
        return False

    return search(tuple(range(len(moduli))), universe, {})


def _divisors(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if limit % n == 0]


def modulus_sets(k: int, max_lcm: int) -> list[tuple[int, ...]]:
    """Every irreducible k-modulus covering whose lcm is at most max_lcm."""
    found: list[tuple[int, ...]] = []
    for span in range(2, max_lcm + 1):
        divisors = _divisors(span)
        def choose(start: int, chosen: list[int]) -> None:
            if len(chosen) == k:
                if reduce(lcm, chosen) != span:
                    return
                moduli = tuple(chosen)
                if is_irreducible_covering(moduli):
                    found.append(moduli)
                return
            for index in range(start, len(divisors)):
                chosen.append(divisors[index])
                choose(index + 1, chosen)
                chosen.pop()
        choose(0, [])
    return found


def summary(sets: list[tuple[int, ...]]) -> dict:
    if not sets:
        return {"count": 0}
    lcms = [reduce(lcm, moduli) for moduli in sets]
    sums = [sum(1 / n for n in moduli) for moduli in sets]
    best = max(range(len(sets)), key=lambda i: (sums[i], tuple(sorted(sets[i]))))
    return {
        "count": len(sets),
        "min_lcm": min(lcms),
        "max_lcm": max(lcms),
        "max_reciprocal": sums[best],
        "max_set": sets[best],
    }
