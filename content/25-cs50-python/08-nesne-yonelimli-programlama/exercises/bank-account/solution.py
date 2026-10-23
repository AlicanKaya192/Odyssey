class Account:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def __str__(self):
        return f"{self.owner}: {self.balance}"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            raise ValueError("Invalid amount")
        self.balance -= amount
