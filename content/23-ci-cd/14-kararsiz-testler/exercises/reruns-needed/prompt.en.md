A test fails with probability `rate` on every run. The chance of seeing it fail at least once in `n` runs is `1 - (1 - rate) ** n`.

Write the function `reruns_needed(rate, confidence=0.95)`: it should return the **smallest** `n` for which this chance reaches or passes `confidence`. If `rate` is 0 or less the test never fails: `None`.

**Expected output:**

```
0.5 5
0.1 29
0.02 149
0.1 44
0.0 None
```
