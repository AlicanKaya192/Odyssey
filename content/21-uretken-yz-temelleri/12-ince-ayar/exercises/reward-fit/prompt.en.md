`fit_reward(diffs, steps, lr)` should learn the reward weights from a list
whose every row is the feature difference "preferred − not preferred": `w`
starts at zero; at every step `p = 1 / (1 + exp(-D @ w))`,
`w += lr * D.T @ (1 - p) / len(D)`. Return the weights as a list of `float`s
rounded to 2 places.

**Expected output:**

```
[9.3, 4.44]
```
