`recall_at_k(ranks, k)` should take the list holding the rank of every
question's right chunk (`None` if it was not found) and return the share of
questions whose rank is not greater than `k`, as a `float` rounded to 2
places.

**Expected output:**

```
1 0.4
3 0.6
5 0.8
```
