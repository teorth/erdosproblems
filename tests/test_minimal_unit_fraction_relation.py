#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from minimal_unit_fraction_relation import ISSUE_PREFIX, has_minimal_signing, largest


def test_issue_354_problem_319_through_n_19():
    assert [largest(n) for n in range(1, 20)] == ISSUE_PREFIX


def test_issue_354_signed_witnesses():
    # The size-8 relation at N = 15, and the size-10 relation at N = 18.
    assert has_minimal_signing((1, 2, 3, 4, 5, 10, 12, 15))
    assert has_minimal_signing((1, 3, 4, 5, 6, 9, 10, 12, 15, 18))
    # The 9-element set named in the issue has an equal split and is not minimal.
    assert not has_minimal_signing((1, 2, 3, 4, 5, 6, 10, 12, 15))


if __name__ == "__main__":
    test_issue_354_signed_witnesses()
    test_issue_354_problem_319_through_n_19()
    print("ok - problem 319")
