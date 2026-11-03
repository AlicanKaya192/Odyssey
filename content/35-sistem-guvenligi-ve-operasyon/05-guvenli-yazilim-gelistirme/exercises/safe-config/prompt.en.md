`load_config(user_config)` should start from the secure defaults
(`DEFAULTS`); of the settings the user gives, it should apply only keys
that are in `DEFAULTS`. Also, `session_minutes` must never exceed 60 (if a
larger value is given, it becomes 60). The starter code accepts every key
as it is.

**Expected output:**

```
debug True
session_minutes 60
tls True
```
