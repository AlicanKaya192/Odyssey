`add_fractions(items)` adds up fraction strings like `"1/3"`, but because it
uses `float`, the result is not a fraction but an approximate decimal like
`0.3333333333333333`. Rewrite it with `Fraction`; return the result as a simplified
fraction string (`"1/2"`). If the total is a whole number, `Fraction` writes
it as `"1"`.

**Expected output:**

```
1/2
7/8
```
