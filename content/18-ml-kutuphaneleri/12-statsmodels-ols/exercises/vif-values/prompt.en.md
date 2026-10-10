`vif_values(columns)` should return the VIF values of the given columns in order (1
place). statsmodels' VIF is computed on data **with a constant column**:
first `sm.add_constant`, then the index starts at 1 (0 is `const`). The
starter code does not add the constant; the values come out wrong.

**Expected output:**

```
[79.1, 78.9, 1.0]
[1.0, 1.0]
```
