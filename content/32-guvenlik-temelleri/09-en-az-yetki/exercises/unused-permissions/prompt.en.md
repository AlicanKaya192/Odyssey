`unused_permissions(granted, used)` should return the granted
privileges (`granted`) that were never used in the logs (not in `used`),
without repeats and in alphabetical order. Both arguments are lists.

**Expected output:**

```
['crm:write']
['a']
```
