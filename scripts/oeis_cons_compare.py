#!/usr/bin/env python3
"""Compare a rational against an OEIS `cons` (decimal expansion) entry.

OEIS keyword:cons sequences store digits *truncated*, not rounded. Common
printers (mpmath.nstr, f-strings, format) round, so a correct constant can
disagree with OEIS on the last digit whenever the next digit is >= 5.

This helper truncates via Decimal and reports whether a mismatch is that
rounding artefact or a genuine non-match.
"""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_UP
from fractions import Fraction


def digits_truncated(value: Fraction, n: int) -> str:
    """Return the first n significant digits of value, truncated."""
    if n <= 0:
        raise ValueError("n must be positive")
    if value <= 0:
        raise ValueError("value must be positive")

    getcontext().prec = n + 20
    d = Decimal(value.numerator) / Decimal(value.denominator)
    # Scientific form so we always get significant digits, not a fixed scale.
    normalized = d.normalize()
    # Digits without exponent: use to_integral / quantize on significand.
    sign, digits, exp = normalized.as_tuple()
    digit_str = "".join(str(x) for x in digits)
    if len(digit_str) < n:
        # Need more fractional digits from a higher precision render.
        getcontext().prec = max(n + 20, getcontext().prec)
        d = Decimal(value.numerator) / Decimal(value.denominator)
        # floor(d * 10^(n-1-floor(log10(d))))
        from math import floor, log10

        log = floor(log10(float(d)))
        scale = Decimal(10) ** (n - 1 - log)
        scaled = (d * scale).to_integral_value(rounding=ROUND_DOWN)
        digit_str = format(int(scaled), "d")
        if len(digit_str) > n:
            digit_str = digit_str[:n]
        elif len(digit_str) < n:
            digit_str = digit_str.ljust(n, "0")
    return digit_str[:n]


def digits_rounded(value: Fraction, n: int) -> str:
    """Return the first n significant digits of value, rounded half-up."""
    if n <= 0:
        raise ValueError("n must be positive")
    if value <= 0:
        raise ValueError("value must be positive")
    getcontext().prec = n + 20
    d = Decimal(value.numerator) / Decimal(value.denominator)
    from math import floor, log10

    log = floor(log10(float(d)))
    scale = Decimal(10) ** (n - 1 - log)
    scaled = (d * scale).to_integral_value(rounding=ROUND_HALF_UP)
    digit_str = format(int(scaled), "d")
    if len(digit_str) > n:
        # Rounding carried into an extra digit (e.g. 999... -> 1000...).
        digit_str = digit_str[:n]
    elif len(digit_str) < n:
        digit_str = digit_str.ljust(n, "0")
    return digit_str[:n]


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
