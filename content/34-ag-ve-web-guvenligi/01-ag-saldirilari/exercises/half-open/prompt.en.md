`events` is a list where each item is `[kind, src]`; `kind` is
`"SYN"` or `"ACK"`. `half_open(events)` should return the sources that sent
a SYN and no ACK after it. Order them by address:
`sorted(..., key=ipaddress.ip_address)` (text order puts `.10` before
`.9`).

**Expected output:**

```
198.51.100.9
198.51.100.10
198.51.100.11
```
