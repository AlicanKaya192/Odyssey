The bin shares of the reference and the current data are given in the same order. Write the function `psi_from_shares(reference, current)`:

- Apply a floor of at least `0.0001` to every share (so there's no `log(0)` for an empty bin).
- Return the sum `Σ (current - reference) × ln(current / reference)`, rounded to three digits.

**Expected output:**

```
0.0
0.228
4.257
```
