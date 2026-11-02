An employee is leaving. `accounts` is system → users, `secrets` is
shared secret → the users who know it.

`leaver_checklist(user, accounts, secrets)` should return the tasks as a
list: first `"disable <system>"` for every system where the user has an
account, then `"rotate <secret>"` for every secret they know. Each group in
alphabetical order. An empty list if there is nothing.

**Expected output:**

```
disable mail
disable wiki
rotate deploy-key
rotate shared-printer
[]
```
