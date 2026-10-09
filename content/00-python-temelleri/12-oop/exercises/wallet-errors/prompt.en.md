Write an error class named `InsufficientFunds` that derives from
`Exception`. Then fix the `spend(amount)` method of the `Wallet` class:

- If `amount` is 0 or less, raise `ValueError("amount must be positive")`.
- If `amount` is larger than the balance, raise
  `InsufficientFunds(f"balance {self.balance}, wanted {amount}")`.
- Otherwise subtract the amount from the balance.

When an error is raised the balance must **not change**. The code at the
bottom tries three purchases; the expected output:

```
spent 20
ValueError: amount must be positive
InsufficientFunds: balance 30, wanted 100
30
```
