`effect(column)` should train the OLS model with a constant term (`sm.add_constant`)
and return `[coefficient, p, low, high]` for the given column (95% interval,
all with 3 places). The starter code forgets the constant; the coefficients
shift.

**Expected output:**

```
[2.934, 0.0, 2.778, 3.089]
[-4.147, 0.253, -11.29, 2.996]
```
