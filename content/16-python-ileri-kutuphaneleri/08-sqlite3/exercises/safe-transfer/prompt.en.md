`transfer(balances, src, dst, amount)` builds the accounts; your job is
the transfer: add `amount` to `dst` and subtract it from `src`. Both updates
go in **one transaction** (`with conn:`); if the `CHECK` constraint breaks,
catch `sqlite3.IntegrityError` so the transaction is undone. At the end,
return `dict(conn.execute("SELECT name, balance FROM accounts"))`.

**Expected output:**

```
{'ada': 70, 'alan': 50}
{'ada': 100, 'alan': 20}
```
