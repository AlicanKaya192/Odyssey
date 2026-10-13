`idf_ends(k)` should return the `k` words with the **lowest** IDF and the `k`
words with the **highest** IDF in the tickets: `[lows, highs]`, both sorted
by IDF from small to large. Use `np.argsort(..., kind="stable")` so that
equal IDFs keep their order.

**Expected output:**

```
the, my, for, order, ord
watiing, webstie, whree, wlil, wokring
```
