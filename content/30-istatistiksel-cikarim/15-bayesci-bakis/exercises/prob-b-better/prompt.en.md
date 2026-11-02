A checkout test with 1500 per group (`make_checkout_test(n=1500, seed=511)`).
Draw 100,000 samples from each posterior with a flat prior (A first). Print
P(B > A) with 3 places and the 95% credible interval of the difference with
4 places.

**Expected output:**

```text
0.97
-0.0009 0.0462
```
