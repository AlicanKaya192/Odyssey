Write the function `variance(values)` with **two passes**: first the mean,
then the mean of the squared deviations from the mean (divide by `n`). It
returns `round(..., 4)`.

No `var`, no `std`. On the data around a billion on the last line, the formula
`E[x²] − (E[x])²` gives a wrong result.

**Expected output:**

```
4.0
0.9911
```
