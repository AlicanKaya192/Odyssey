`kl_term(mu, logvar)` should return the KL term of a single code as a
`float` rounded to 4 places: `0.5 * (mu ** 2 + exp(logvar) - logvar - 1)`,
summed over every dimension.

**Expected output:**

```
0.0
2.0
0.5677
```
