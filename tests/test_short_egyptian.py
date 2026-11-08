#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from short_egyptian import ISSUE_PREFIX, f


def test_issue_271_through_k_21():
    for k, want in ISSUE_PREFIX.items():
        assert f(k) == want, (k, f(k), want)


if __name__ == "__main__":
    test_issue_271_through_k_21()
    print("ok - short egyptian")
