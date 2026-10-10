import unittest

from bank import Account


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(100)

    # cekim, fazla cekim (ValueError), tam bakiye kadar cekim
