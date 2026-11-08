#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from short_egyptian import (
    ISSUE_PREFIX,
    _exists,
    _harmonic_short,
    decomposition,
    f,
    split_largest,
    sums_to_one,
)


def test_issue_271_through_k_21():
    for k, want in ISSUE_PREFIX.items():
        assert f(k) == want, (k, f(k), want)
        assert decomposition(k)[0] == want
        assert sums_to_one(decomposition(k))


def test_issue_271_k_22_by_splitting():
    # f(21) = 11, and splitting its largest term keeps the same minimum.
    extended = split_largest(decomposition(21))
    assert extended[0] == 11 and len(extended) == 22 and sums_to_one(extended)
    # 12 and 13 are impossible. Every larger first term is shorter than the harmonic tail.
    assert not _exists(21, 11, 12, 13)
    assert not _exists(21, 12, 13, 14)
    assert all(_harmonic_short(21, n1 - 1, n1, n1 + 1) for n1 in range(14, 23))


if __name__ == "__main__":
    test_issue_271_through_k_21()
    print("ok - short egyptian")
