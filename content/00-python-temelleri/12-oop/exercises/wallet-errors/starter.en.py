# Define the InsufficientFunds error class here


class Wallet:
    def __init__(self, balance):
        self.balance = balance

    def spend(self, amount):
        # Check first, raise an error if needed
        self.balance = self.balance - amount


wallet = Wallet(50)
for amount in [20, -5, 100]:
    try:
        wallet.spend(amount)
        print("spent", amount)
    except ValueError as error:
        print("ValueError:", error)
    except InsufficientFunds as error:
        print("InsufficientFunds:", error)
print(wallet.balance)
