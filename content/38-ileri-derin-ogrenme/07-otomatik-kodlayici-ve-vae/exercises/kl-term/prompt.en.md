`kl_term(mu, logvar)` should compute the KL term from the lesson (`(B, D)`
inputs): `-0.5 · mean_B( sum_D(1 + logvar − mu² − e^logvar) )`. Return it with
3 places; add `+ 0.0` to the result so that minus zero is not printed.

**Expected output:**

```
2.0
0.0
```
