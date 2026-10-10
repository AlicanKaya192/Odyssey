`size_report(sizes)` should turn the sizes into an **ordered category** in
the order `S < M < L < XL` (`pd.CategoricalDtype([...], ordered=True)`).
Return:

- `"sorted"`: the list sorted by size
- `"large"`: the number that are `L` or larger (`int`)
- `"max"`: the largest size

**Do not write a loop.**

**Expected output:**

```
['S', 'M', 'M', 'L', 'XL']
2 XL
```
