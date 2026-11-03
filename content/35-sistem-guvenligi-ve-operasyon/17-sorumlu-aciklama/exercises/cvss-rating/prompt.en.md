`cvss_rating(score)` should turn the score into a rating: `0` →
`"none"`, 0.1–3.9 `"low"`, 4.0–6.9 `"medium"`, 7.0–8.9 `"high"`,
9.0–10.0 `"critical"`. The starter code is wrong at the boundaries.

**Expected output:**

```
0 none
3.9 low
4.0 medium
6.9 medium
7.0 high
8.9 high
9.0 critical
10.0 critical
```
