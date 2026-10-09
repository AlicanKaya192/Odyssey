Write the function `mnb_predict(C, y, Cq, alpha)`: with the log priors and
word log probabilities, return for each query row the class where
`prior + Cq @ logw.T` is largest, as a list of `int`s.

No `MultinomialNB`.

**Expected output:**

```
[0, 1, 0]
```
