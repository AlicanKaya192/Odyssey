The context manager `timed(results, label)` writes the block's duration to
`results[label]`, but not when an error occurs in the block. Fix the tidying
up with `try/finally`: the duration must be recorded in every case.

**Expected output:**

```
['failed', 'ok']
```
