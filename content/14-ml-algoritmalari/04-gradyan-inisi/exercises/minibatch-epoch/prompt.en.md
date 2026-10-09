Write the function `minibatch_epoch(A, y, w, lr, batch, seed)`: one epoch of
mini-batch gradient descent. The order is
`np.random.default_rng(seed).permutation(n)`; take groups from the starts
`0, batch, 2·batch, …`, and in each group take one step with that group's MSE
gradient (`2/len(group)`). Return `.round(4).tolist()`.

**Expected output:**

```
[0.5286, 3.0044]
[0.5863, 3.2303]
[0.6083, 3.2057]
```
