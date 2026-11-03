`classify(text)` should return `"loopback"` if the address is
loopback, `"private"` if it is private, and `"public"` otherwise
(`is_loopback`, `is_private`). The starter code runs but gives the wrong
answer for `127.0.0.1`; find out why.

**Expected output:**

```
127.0.0.1 loopback
10.1.2.3 private
172.31.0.9 private
172.32.0.9 public
100.20.30.40 public
```
