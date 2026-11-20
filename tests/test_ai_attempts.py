#!/usr/bin/env python3
"""AI attempt labels follow the informal status, including decidable."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_readme import ai_attempts_link


def test_decidable_matches_the_other_finitary_open_states():
    decidable = ai_attempts_link("19", "decidable")
    falsifiable = ai_attempts_link("23", "falsifiable")
    verifiable = ai_attempts_link("1", "verifiable")
    assert "](https://mehmetmars7.github.io/Erdosproblems-llm-hunter/problem.html?type=erdos&id=19)" in decidable
    assert decidable.startswith("[view](")
    assert falsifiable.startswith("[view](")
    assert verifiable.startswith("[view](")


def test_settled_problems_stay_add():
    assert ai_attempts_link("2", "proved").startswith("[add](")
    assert ai_attempts_link("3", "disproved").startswith("[add](")
    assert ai_attempts_link("4", "solved").startswith("[add](")


if __name__ == "__main__":
    test_decidable_matches_the_other_finitary_open_states()
    test_settled_problems_stay_add()
    print("ok - ai attempts")
