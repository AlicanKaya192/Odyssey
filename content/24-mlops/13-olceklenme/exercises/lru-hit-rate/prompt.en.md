Write the function `hit_rate(requests, size)` that computes the hit rate of the lesson's LRU cache:

- `requests`: the keys asked in order, `size`: the number of entries the cache can hold.
- If the key is in the cache, count a hit and move it to the end.
- Otherwise add it; if the cache exceeds `size`, remove the first one (the one asked about least recently).
- Return the ratio of hits to requests, rounded to three digits.

**Expected output:**

```
0.0
0.2
0.5
```
