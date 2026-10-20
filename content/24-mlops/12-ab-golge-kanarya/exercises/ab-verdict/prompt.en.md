Write the function `ab_verdict(diff, aa_gaps)` that interprets an A/B difference with the A/A noise:

- `aa_gaps`: the gaps measured in the A/A test (positive numbers).
- The band: the value at position `int(0.95 * length)` in the sorted gaps, rounded to three digits.
- If the absolute value of `diff` is greater than the band, return `["real", band]`, otherwise `["noise", band]`.

**Expected output:**

```
['real', 0.095]
['noise', 0.095]
['real', 0.095]
```
