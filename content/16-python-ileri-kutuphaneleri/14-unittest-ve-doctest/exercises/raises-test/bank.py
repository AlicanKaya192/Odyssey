class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("not enough money")
        self.balance -= amount
