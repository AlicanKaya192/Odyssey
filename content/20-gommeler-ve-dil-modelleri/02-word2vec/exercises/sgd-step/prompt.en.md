`sgd_step(v, u_pos, u_negs, lr)` should apply the lesson's update for one
pair:

- `g_pos = σ(v · u_pos) − 1`, for each negative `g_k = σ(v · u_k)`
- the derivative for `v` is `g_pos · u_pos + Σ g_k · u_k`
- `u_pos ← u_pos − lr · g_pos · v`, `u_k ← u_k − lr · g_k · v`,
  `v ← v − lr · derivative` (all with the **old** values)

Return the three results as lists with 3 places: `[v, u_pos, u_negs]`.

**Expected output:**

```
[0.517, -0.532]
[1.013, -1.013]
[[0.174, 0.126]]
```
