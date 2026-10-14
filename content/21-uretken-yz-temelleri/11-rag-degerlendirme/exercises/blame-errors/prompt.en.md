`blame(cases, k)` should put every `[correct, rank]` pair into one of three
groups and return `[correct, retrieval miss, reading error]`. If correct, it is
correct; otherwise, if the rank is `None` or greater than `k`, a retrieval
miss, else a reading error.

**Expected output:**

```
[2, 2, 1]
```
