`similarity(a, b, n)` should return the Jaccard similarity (common / union) of
the two words' character n-gram sets, rounded to 2 places. `char_ngrams` is
ready. The output shows `n=3` and `n=2` side by side for the same pairs.

**Expected output:**

```
cable 1.0 1.0
cables 0.57 0.62
cabel 0.25 0.33
able 0.5 0.57
```
