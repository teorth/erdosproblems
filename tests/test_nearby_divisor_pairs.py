#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from nearby_divisor_pairs import ISSUE_PREFIX, r

def test_matches_issue_354():
    for n, want in enumerate(ISSUE_PREFIX, 1):
        assert r(n) == want, (n, r(n), want)

def test_a174903_divergence_at_60():
    # A174903 counts partnered divisors, not pairs; first split at n=60.
    assert r(60) == 13

if __name__ == "__main__":
    test_matches_issue_354()
    test_a174903_divergence_at_60()
    print("ok - nearby divisor pairs")
