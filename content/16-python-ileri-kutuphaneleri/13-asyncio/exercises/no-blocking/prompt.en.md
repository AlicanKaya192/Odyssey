`tick(n)` contains `time.sleep(0.2)`; even though `gather` is used, the four
jobs run one after another (0.8 s). Change the waiting line so it does not
block the event loop. The expected output:

```
[0, 1, 2, 3] True
```

**Expected output:**

```
[0, 1, 2, 3] True
```
