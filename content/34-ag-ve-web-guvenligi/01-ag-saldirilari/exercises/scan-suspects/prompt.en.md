`log` holds connection records, each `[src, port]`.
`suspects(log, limit)` should return, in address order
(`key=ipaddress.ip_address`), the sources that touched at least `limit`
**different** ports. Repeats to the same port count once.

**Expected output:**

```
['198.51.100.10']
['198.51.100.9', '198.51.100.10']
```
