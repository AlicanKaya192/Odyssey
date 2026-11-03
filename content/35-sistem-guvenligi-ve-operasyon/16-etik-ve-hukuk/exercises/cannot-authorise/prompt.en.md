`owners` is system → owner. `cannot_authorise(owners, signed_by,
targets)` should return, in alphabetical order, the targets the signer
**cannot** authorise: those owned by someone else and those whose owner is
not known at all (not in `owners`).

**Expected output:**

```
['shop.example.org', 'vpn.example.org']
```
