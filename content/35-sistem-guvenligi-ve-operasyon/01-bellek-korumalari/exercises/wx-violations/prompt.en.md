`regions` is region name → permission string (like `"r-x"`).
`wx_violations(regions)` should return the names of the regions that are
**both writable and executable**, as a list in alphabetical order. The
starter code only looks at `x` and flags the code region too.

**Expected output:**

```
['jit', 'plugin']
```
