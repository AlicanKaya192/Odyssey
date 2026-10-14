`kept_share(k)` should return, from the singular values (`S`) of the training
data (mean subtracted), how much of the data's spread the first `k`
directions keep: `(S[:k] ** 2).sum() / (S ** 2).sum()`, as a `float` rounded
to 3 places.

**Expected output:**

```
2 0.287
8 0.674
16 0.85
32 0.966
```
