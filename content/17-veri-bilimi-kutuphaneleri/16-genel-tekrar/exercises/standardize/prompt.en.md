`standardize(rows)` should standardise each **column** of the number table:
subtract the column mean and divide by the column standard deviation
(`X.mean(axis=0)`, `X.std(axis=0)`, with broadcasting). Return the result as
a list of lists rounded to 2 places. The starter code gives no `axis`: it
uses one mean for the whole table. **Do not write a loop.**

**Expected output:**

```
[-1.22, -1.22]
[0.0, 0.0]
[1.22, 1.22]
```
