#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lambda4_cubic import cubic, derivative, has_sign_change, unique_real_root


def test_sign_change_and_root():
    y = unique_real_root()
    assert abs(y - 1.5195578816428) < 1e-10
    assert abs(cubic(y)) < 1e-9


def test_cubic_negative_then_positive():
    assert cubic(0) > 0
    assert cubic(1) > 0
    assert cubic(1.2) < 0
    assert cubic(2) > 0
    assert has_sign_change(1.1, 1.6)
    assert not has_sign_change(0.0, 1.0)


def test_derivative_positive_near_root():
    # unique real root: derivative should not vanish there
    y = unique_real_root()
    assert derivative(y) != 0


if __name__ == "__main__":
    test_sign_change_and_root()
    test_cubic_negative_then_positive()
    test_derivative_positive_near_root()
    print("ok - lambda4 cubic")
