A scan's finding scores are a list. The function `cvss_band` is ready in
the starter code.

Write the function `band_summary(scores)`: return a dictionary containing
**all** five severities in this order: `"None"`, `"Low"`, `"Medium"`,
`"High"`, `"Critical"`. The values are how many findings have that
severity; `0` if there are none.

**Expected output:**

```
None 1
Low 1
Medium 1
High 2
Critical 2
```
