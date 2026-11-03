`date_status(cert, today)` should say whether the certificate is valid on
`today`: `"not yet valid"` if `today` is before `not_before`, `"expired"`
if after `not_after`, `"ok"` if in between. The dates are `YYYY-MM-DD`
text. The starter code only looks at the end date.

**Expected output:**

```
ok
not yet valid
expired
```
