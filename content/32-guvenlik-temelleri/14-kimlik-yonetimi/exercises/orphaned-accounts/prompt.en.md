`accounts` is every system's account list (system → user names),
`active` the active employees from human resources.

`orphaned_accounts(accounts, active)` should return every account that is
not active as `"system/user"`, in a list in alphabetical order.

**Expected output:**

```
mail/deniz
payroll/emre
wiki/deniz
```
