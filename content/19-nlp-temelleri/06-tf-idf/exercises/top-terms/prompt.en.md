`top_terms(index, k)` should return the `k` heaviest words in the TF-IDF row of
ticket number `index`, heaviest first, as a list. The vectoriser
(`min_df=2`), `X` and `words` are ready.

**Expected output:**

```
0 ['prague', 'slow', 'very']
1 ['acconut', 'friday', 'reset']
2 ['tracking', 'work', 'with']
```
