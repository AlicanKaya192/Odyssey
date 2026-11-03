`random_source(purpose)` should say which module a value must be made
with: `"secrets"` if `purpose` is `"token"`, `"key"`, `"password"`,
`"nonce"` or `"salt"`, otherwise (games, simulations) `"random"`. The
starter code says `"random"` for everything.

**Expected output:**

```
token secrets
dice random
salt secrets
simulation random
```
