The record format is `pbkdf2_sha256$iterations$salt$key`. `make_record`
is ready. `upgrade(password, record, minimum)` checks the password with the
record's parameters and returns `"wrong password"` if it is wrong. What is
missing: if the password is right and the record's iteration count is
**less than** `minimum`, return a new record with the same salt and
`minimum` iterations; otherwise give the record back unchanged.

**Expected output:**

```
3000
True
wrong password
```
