A program's secure default settings are in the `defaults` dictionary.
The user gives their own settings with the `user` dictionary.

`merge_settings(defaults, user)` should return a **new** dictionary:

- start with all the keys of `defaults`,
- a value from `user` is applied only if the key **exists** in `defaults`;
  unknown keys are dropped,
- the `defaults` dictionary itself must not change.

**Expected output:**

```
debug True
tls True
password_min 12
defaults debug: False
```
