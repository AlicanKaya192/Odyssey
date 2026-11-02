`cvss_band(score)` should turn a CVSS score into a severity name:

- `0.0` → `"None"`, `0.1`–`3.9` → `"Low"`, `4.0`–`6.9` → `"Medium"`,
- `7.0`–`8.9` → `"High"`, `9.0`–`10.0` → `"Critical"`.

The starter code is almost right but gets the boundaries wrong. Look at the
`4.0`, `7.0` and `9.0` lines in the output and fix it.

**Expected output:**

```
0.0 None
2.5 Low
4.0 Medium
6.9 Medium
7.0 High
9.0 Critical
10.0 Critical
```
