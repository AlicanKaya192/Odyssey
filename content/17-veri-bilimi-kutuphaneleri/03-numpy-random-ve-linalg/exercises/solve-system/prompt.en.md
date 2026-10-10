`solve(A, b)` should solve `A x = b` with `np.linalg.solve` and return the
result as a list rounded to 3 places. If the matrix is singular
(`np.linalg.LinAlgError`), return the text `"singular"`.

**Expected output:**

```
[0.8, 1.4]
singular
```
