Write the function `vote_accuracy(n, p)`: the probability that the majority
vote of `n` models (n odd), each right with probability `p` and with
independent errors, is right: `Σ C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ`, for `k` from
`n // 2 + 1` to `n`. `round(..., 3)`. You can use `math.comb`.

**Expected output:**

```
1 0.6
5 0.683
25 0.846
101 0.979
0.306
```
