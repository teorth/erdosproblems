#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from erdos_962 import A327909_PREFIX, a327909, m, sequence_m


def test_matches_oeis_prefix():
    for k, want in enumerate(A327909_PREFIX, 1):
        assert a327909(k) == want, (k, a327909(k), want)
        assert m(k) == want - 1


def test_sequence_helper():
    assert sequence_m(10) == [a - 1 for a in A327909_PREFIX[:10]]


if __name__ == "__main__":
    test_matches_oeis_prefix()
    test_sequence_helper()
    print("ok - erdos 962 / A327909")
