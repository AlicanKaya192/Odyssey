import unittest

from text_tools import word_count


class TestWordCount(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(word_count("a b c"), 3)

    def test_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_spaces(self):
        self.assertEqual(word_count("  a   b "), 2)
