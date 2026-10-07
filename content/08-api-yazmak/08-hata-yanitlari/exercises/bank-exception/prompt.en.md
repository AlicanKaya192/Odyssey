The `accounts` dictionary is ready: `ada` 100, `alan` 20.

**What to do:**

1. An exception class named `InsufficientFunds` with a `balance` field.
2. A `withdraw(name, amount)` helper: if the balance isn't enough it raises
   `InsufficientFunds(balance)`; otherwise it subtracts and returns the new
   balance. **It mustn't know about HTTP.**
3. A handler that turns this exception into the answer `400`,
   `{"error": "insufficient_funds", "balance": ...}`.
4. `POST /accounts/{name}/withdraw?amount=...` → `{"name": ..., "balance": ...}`

- `POST /accounts/ada/withdraw?amount=30` → `{"name": "ada", "balance": 70}`
- `POST /accounts/alan/withdraw?amount=50` → `400`, `{"error": "insufficient_funds", "balance": 20}`
