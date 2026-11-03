`redact(line)` should turn the values of the `password`, `token`,
`secret` and `api_key` fields in a log line into `***`; the key name stays
as it is. Case does not matter (`Token=...` is hidden too). The value is
the part after `=` up to the next space.

**Expected output:**

```
login user=ada password=*** ok
api_key=*** Token=*** status=200
nothing to hide here
```
