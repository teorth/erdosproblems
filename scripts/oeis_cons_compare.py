#!/usr/bin/env python3
"""Compare a rational against an OEIS `cons` (decimal expansion) entry.

OEIS keyword:cons sequences store digits *truncated*, not rounded. Common
printers (mpmath.nstr, f-strings, format) round, so a correct constant can
disagree with OEIS on the last digit whenever the next digit is >= 5.

This helper uses exact integer arithmetic and reports whether a mismatch is that
rounding artefact or a genuine non-match.
"""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


def _scaled_ratio(value: Fraction, n: int) -> tuple[int, int]:
    """Scale a positive rational so its integer part has n significant digits."""
    if n <= 0:
        raise ValueError("n must be positive")
    if value <= 0:
        raise ValueError("value must be positive")

    numerator, denominator = value.numerator, value.denominator
    exponent = len(str(numerator)) - len(str(denominator))
    if exponent >= 0:
        below_power = numerator < denominator * 10**exponent
    else:
        below_power = numerator * 10**(-exponent) < denominator
    if below_power:
        exponent -= 1

    scale = n - 1 - exponent
    if scale >= 0:
        numerator *= 10**scale
    else:
        denominator *= 10**(-scale)
    return numerator, denominator


def digits_truncated(value: Fraction, n: int) -> str:
    """Return the first n significant digits of value, truncated."""
    numerator, denominator = _scaled_ratio(value, n)
    return str(numerator // denominator)


def digits_rounded(value: Fraction, n: int) -> str:
    """Return the first n significant digits of value, rounded half-up."""
    numerator, denominator = _scaled_ratio(value, n)
    digits, remainder = divmod(numerator, denominator)
    if 2 * remainder >= denominator:
        digits += 1
    # A carry can add one digit, e.g. 9999 rounds to 10000.
    return str(digits)[:n]


def compare_cons(value: Fraction, oeis_digits: str) -> dict:
    """Compare value to an OEIS cons digit string.

    Returns a dict with keys:
      match: bool — truncated digits equal OEIS
      truncated: str
      rounded: str
      rounding_false_negative: bool — rounded disagrees but truncated matches
    """
    oeis_digits = "".join(ch for ch in oeis_digits if ch.isdigit())
    n = len(oeis_digits)
    if n == 0:
        raise ValueError("oeis_digits must contain at least one digit")
    truncated = digits_truncated(value, n)
    rounded = digits_rounded(value, n)
    match = truncated == oeis_digits
    return {
        "match": match,
        "truncated": truncated,
        "rounded": rounded,
        "oeis": oeis_digits,
        # Truncated agrees with OEIS, but a rounded print would have disagreed.
        "rounding_false_negative": match and rounded != oeis_digits,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numerator", type=int, help="numerator of the exact Fraction")
    parser.add_argument("denominator", type=int, help="denominator of the exact Fraction")
    parser.add_argument("oeis_digits", help="digit string from the OEIS cons entry (punctuation ignored)")
    args = parser.parse_args(argv)
    result = compare_cons(Fraction(args.numerator, args.denominator), args.oeis_digits)
    if result["rounding_false_negative"]:
        print(
            "TRUNCATION MATCH (rounding would have false-negatived): "
            f"truncated={result['truncated']} rounded={result['rounded']} oeis={result['oeis']}",
            file=sys.stderr,
        )
    elif result["match"]:
        print(f"match: {result['truncated']}")
    else:
        print(
            f"mismatch: truncated={result['truncated']} rounded={result['rounded']} oeis={result['oeis']}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
