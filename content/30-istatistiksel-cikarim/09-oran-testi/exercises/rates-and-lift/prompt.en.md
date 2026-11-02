In the checkout test with 3000 people per group
(`make_checkout_test(n=3000, seed=141)`) print, one per line: the two groups'
rates A and B (4 places, on the same line), the absolute difference
`pB - pA` (4 places) and the relative lift `(pB - pA) / pA` (3 places). The
starter code prints the ratio `pB / pA` instead of the relative lift.

**Expected output:**

```text
0.1207 0.1377
0.017
0.141
```
