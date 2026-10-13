`top_k(sims, k)` should return the **positions** (indices) of the `k` largest
values in the similarity list, largest first. Find the k with
`np.argpartition`, then sort only those.

**Expected output:**

```
[5, 1, 3]
```
