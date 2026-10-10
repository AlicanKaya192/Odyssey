import unittest

from bank import Account


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(100)

    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70)

    def test_too_much(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(500)
        self.assertEqual(self.account.balance, 100)

    def test_exact_balance(self):
        self.account.withdraw(100)
        self.assertEqual(self.account.balance, 0)
