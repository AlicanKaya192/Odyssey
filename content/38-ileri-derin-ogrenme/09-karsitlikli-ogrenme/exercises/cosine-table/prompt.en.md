`cosine_table(vectors)` should bring the vectors to unit length
(`F.normalize`), compute the cosine similarity table (`z @ z.T`) and return
it as a nested list, every value with 2 places.

**Expected output:**

```
[[1.0, 0.71], [0.71, 1.0]]
```
