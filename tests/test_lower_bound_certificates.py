#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lower_bound_certificates import SIDON_SETS, SUNFLOWER_FREE, is_sidon, is_sunflower_free


def test_issue_473_sidon_certificates():
    for limit, values in SIDON_SETS.items():
        assert is_sidon(values, limit), limit
    assert [len(SIDON_SETS[n]) for n in (100, 250, 500, 1000)] == [12, 17, 22, 28]


def test_issue_473_sunflower_free_families():
    for (k, universe), family in SUNFLOWER_FREE.items():
        assert is_sunflower_free(family, k, universe)
    # A sunflower-free family of size m forces the 3-sunflower number to be at least m + 1.
    assert len(SUNFLOWER_FREE[(3, 9)]) + 1 == 15
    assert len(SUNFLOWER_FREE[(4, 11)]) + 1 == 31


if __name__ == "__main__":
    test_issue_473_sidon_certificates()
    test_issue_473_sunflower_free_families()
    print("ok - certificates")
