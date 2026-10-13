`oov_shares(n_train)` should build the vocabulary **from the first `n_train`
reviews only**. Then return the share of tokens not in the vocabulary (3
places) in two groups of text as `[reviews, tickets]`: the reviews are
`REVIEWS[1000:]`, the tickets `TICKETS`. Tokens come from the vectoriser's
`build_analyzer()`.

The starter code fits on all the reviews; it has seen the test reviews too.

**Expected output:**

```
50 [0.078, 0.637]
200 [0.012, 0.636]
1000 [0.005, 0.635]
```
