`original` and `restored` are file name → content (text).
`restore_check(original, restored)` should return lines in alphabetical
order by name: for every file with an original `"<name>: ok"`,
`"<name>: different"` or `"<name>: missing"`; for a file only in the
restored set `"<name>: extra"`. Compare contents by their SHA-256
hashes.

**Expected output:**

```
keys.txt: missing
orders.csv: ok
tmp.log: extra
users.csv: different
```
