`precise_divide(a, b, digits)` turns two strings into `Decimal`s, divides
them and returns the result as text; the division must use `digits`
**significant digits**. Because the starter code changes `getcontext().prec`,
the precision of the whole program breaks (the last line should print 28).
Use `localcontext()`.

**Expected output:**

```
0.14286
0.667
28
```
