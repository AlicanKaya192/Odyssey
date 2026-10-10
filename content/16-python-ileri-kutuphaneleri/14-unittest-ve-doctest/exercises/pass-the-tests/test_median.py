import unittest

from main import median


class TestMedian(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_even(self):
        self.assertEqual(median([4, 1, 3, 2]), 2.5)

    def test_single(self):
        self.assertEqual(median([7]), 7)

    def test_empty(self):
        with self.assertRaises(ValueError):
            median([])
