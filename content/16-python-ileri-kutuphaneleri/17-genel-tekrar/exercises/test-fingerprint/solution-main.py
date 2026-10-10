import unittest

from tools import fingerprint


class TestFingerprint(unittest.TestCase):
    def test_length(self):
        self.assertEqual(len(fingerprint("hello")), 12)

    def test_same_text(self):
        self.assertEqual(fingerprint("Hello"), fingerprint("  hello  "))

    def test_different_text(self):
        self.assertNotEqual(fingerprint("hello"), fingerprint("hello!"))
