Fix `logging.basicConfig` so it writes logs to **stdout**, from the
`INFO` level up, in the format `"%(levelname)s: %(message)s"`. The `debug`
message must not appear; `info` and `warning` must.

**Expected output:**

```
INFO: job started
WARNING: low memory
```
