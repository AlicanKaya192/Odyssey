`rto_check(size_gb, speed, setup, rto)` should calculate the restore time
with `setup + size_gb / speed` and return `[time, meets]`: the time
rounded to 1 place, and the second `True` if the time does not exceed
`rto`.

**Expected output:**

```
[7.5, False]
[2.5, True]
```
