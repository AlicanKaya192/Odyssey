`delay_after(failures, start, cap)` should return `0` if the number of
failed attempts is less than `start`, and otherwise
`2 ** (failures - start)` seconds; but never more than `cap`.

**Expected output:**

```
[0, 0, 1, 2, 4, 8, 16]
300
```
