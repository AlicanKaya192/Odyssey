Write the function `bic_choice(logliks, n)`: `logliks[i]` is the
log-likelihood of `k = i + 1` components in a 1-D GMM. The number of
parameters is `p = 3k − 1`, `BIC = p · ln n − 2 · log-likelihood`. Return
`(the BIC list round(..., 1), the k of the smallest BIC)`.

**Expected output:**

```
[2282.2, 2159.9, 2177.3, 2192.4, 2204.8]
2
```
