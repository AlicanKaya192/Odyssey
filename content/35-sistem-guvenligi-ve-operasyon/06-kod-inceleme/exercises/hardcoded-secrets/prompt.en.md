`hardcoded_secrets(source)` should return, in alphabetical order, the
variable names of assignments whose name contains (case does not matter)
`password`, `secret` or `token` and whose value is a **fixed string**. If
the value comes from a function or is not a string (a number), it does not
count.

**Expected output:**

```
['SECRET_KEY', 'db_password']
```
