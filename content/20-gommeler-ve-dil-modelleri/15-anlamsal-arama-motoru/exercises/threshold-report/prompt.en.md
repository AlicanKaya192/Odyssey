`threshold_report(inside, outside, loss)` should pick the threshold from the
real tickets' (`inside`) scores: the value at position `int(loss · length)` of
the sorted list. Then return `[threshold, share of real tickets at or above
it, share of unrelated texts below it]` (shares with 3 places).

**Expected output:**

```
[0.3, 0.9, 0.6]
[0.4, 0.7, 0.8]
```
