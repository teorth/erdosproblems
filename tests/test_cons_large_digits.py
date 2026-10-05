import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('cons', Path(__file__).parents[1] / 'scripts' / 'oeis_cons_compare.py')
cons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cons)

class LongDecimalTests(unittest.TestCase):
    def test_long_repeating_prefix(self):
        self.assertEqual(cons.digits_truncated(Fraction(1, 3), 5000), '3' * 5000)
        self.assertEqual(cons.digits_rounded(Fraction(1, 3), 5000), '3' * 5000)

    def test_large_fraction_components(self):
        value = Fraction(10**5000 + 1, 10**5001 + 30)
        self.assertEqual(cons.digits_truncated(value, 5), '99999')
        self.assertEqual(cons.digits_rounded(value, 5), '10000')

if __name__ == '__main__':
    unittest.main()
