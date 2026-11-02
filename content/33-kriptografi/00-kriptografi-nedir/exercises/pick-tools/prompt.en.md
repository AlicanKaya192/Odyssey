`needs` is a dictionary; a missing key counts as `False`.
`pick_tools(needs)` should return the alphabetically sorted list of the
tools needed:

- `secret` → `"encryption"`
- `password` → `"password-hash"`
- `third_party` (proof to a third party) → `"signature"`
- `tamper` and not `third_party` → `"mac"

**Expected output:**

```
['encryption']
['mac']
['signature']
['encryption', 'password-hash']
[]
```
