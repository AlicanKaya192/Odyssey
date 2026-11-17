`standardize(rows)` should subtract each **column**'s mean and divide by its
standard deviation (biased, `unbiased=False`). Broadcasting applies it to the
whole table in one line. Return a list of lists with 2 places.

**Expected output:**

```
[-1.22, -1.22]
[0.0, 1.22]
[1.22, 0.0]
```
