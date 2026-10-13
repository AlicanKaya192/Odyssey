`ppmi(count_ab, count_a, count_b, total)` should compute the PPMI of two words:
`log(count_ab · total / (count_a · count_b))`, `0` if negative. If they never
appeared together (`count_ab == 0`), `0.0`. 3 places.

**Expected output:**

```
3.219
0.0
0.0
```
