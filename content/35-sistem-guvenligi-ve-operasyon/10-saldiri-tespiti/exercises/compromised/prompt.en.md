Each event is `[time, ip, user, result]`; the result is `"fail"` or
`"ok"`. `compromised(events, threshold)` should return, in event order, a
`"<time> <user> <ip>"` line for every successful login that comes **after**
at least `threshold` failures from the same `(ip, user)` pair. After a
successful login, that pair's counter resets.

**Expected output:**

```
10:04 bob 203.0.113.9
```
