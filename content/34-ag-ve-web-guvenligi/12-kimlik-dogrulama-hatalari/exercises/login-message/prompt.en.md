`hash_pw` and `DUMMY` are ready. `login(users, user, password)` should
return `"welcome"` if the user exists and the password's hash matches the
stored hash with `hmac.compare_digest`, and otherwise **in every case**
`"invalid user name or password"`. A hash must be computed for an unknown
user too: compare with `DUMMY`. The starter code gives different
messages.

**Expected output:**

```
welcome
invalid user name or password
invalid user name or password
```
