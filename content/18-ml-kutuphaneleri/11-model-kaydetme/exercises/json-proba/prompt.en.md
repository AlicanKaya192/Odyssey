`TEXT` holds the logistic pipeline's parameters as JSON (`mean`, `scale`, `coef`,
`intercept`). `json_proba(rows)` should compute the probabilities from this
text and NumPy only (3 places): scale first (`(x - mean) / scale`), then
multiply by the coefficients, add the constant, sigmoid. The starter code
skips scaling.

**Expected output:**

```
[0.293, 0.817]
```
