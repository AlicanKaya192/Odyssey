`contact_status(fields, now)` takes the parsed fields and the current
time (ISO, with `Z`) and returns, in order: `"no contact"` if there is no
contact, `"no expiry"` if there is no `expires`, `"expired"` if the time
has passed or ends exactly now, otherwise `"ok"`. The starter code never
compares the time.

**Expected output:**

```
ok
expired
no contact
```
