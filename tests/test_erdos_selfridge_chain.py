#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from erdos_selfridge_chain import (
    ISSUE_ALL_PRIME,
    ISSUE_LENGTHS,
    all_terms_prime,
    chain,
    chain_length,
    is_prime,
)


def test_matches_issue_354_lengths():
    for i, want in enumerate(ISSUE_LENGTHS):
        n = i + 3
        assert chain_length(n) == want, (n, chain_length(n), want)


def test_matches_issue_354_all_prime():
    got = [n for n in range(3, 81) if all_terms_prime(n)]
    assert got == ISSUE_ALL_PRIME


def test_n8_example():
    # Erdős–Graham / site example: n=8 gives 7, 5
    assert chain(8) == [7, 5]
    assert all(is_prime(a) for a in chain(8))


if __name__ == "__main__":
    test_matches_issue_354_lengths()
    test_matches_issue_354_all_prime()
    test_n8_example()
    print("ok - erdos selfridge chain")
