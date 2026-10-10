`robust_scale(values)` should scale single-column data in an **outlier-proof**
way (`RobustScaler`: subtract the median, divide by the interquartile range)
and return a list rounded to 2 places. The starter code uses
`StandardScaler`; a single large value squeezes the others.

**Expected output:**

```
[-1.0, -0.5, 0.0, 0.5, 46.0]
```
