import unittest

from bank import Account


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(100)

    # withdraw, withdraw too much (ValueError), withdraw exactly the balance
