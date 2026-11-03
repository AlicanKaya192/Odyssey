`connections` are `[host, port]` attempts from inside to outside, and
`allowed` the allowed ports. `blocked(connections, allowed)` should return
the blocked attempts as `"host:port"` texts: in the order first seen and
**without repeats**.

**Expected output:**

```
192.168.1.10:8888
192.168.1.30:2525
```
