`vif_values(columns)` should return the VIF values of the given columns in order (1
place). Code often adds a constant column with `sm.add_constant` first (older
statsmodels versions needed it for a correct VIF; 0.15 corrects the result
itself). Adding the constant shifts the index: column 0 is `const`, the given
columns start at 1. The starter code adds the constant but starts the index at
0; the first value is the one for `const` and the last column never appears.

**Expected output:**

```
[79.1, 78.9, 1.0]
[1.0, 1.0]
```
