`top_p_filter(probs, p)` should walk the words from largest to smallest and add
up their probabilities; stop at the first word where the total reaches (or
passes) `p`. Rescale the kept words' probabilities to sum to 1 (3
places).

**Expected output:**

```
0.75 order=0.625 parcel=0.375
0.4 order=1.0
1.0 order=0.5 parcel=0.3 box=0.15 app=0.05
```
