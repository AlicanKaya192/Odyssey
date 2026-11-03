`safe_update(user, changes, allowed)` should return a **copy** of the
user; of the fields in `changes` it should write only those in the
`allowed` list. The original `user` dict must not change. The starter code
writes every field into the original dict: the `role` in the request makes
the user an administrator.

**Expected output:**

```
ada@x.io user
a@x.io user
```
