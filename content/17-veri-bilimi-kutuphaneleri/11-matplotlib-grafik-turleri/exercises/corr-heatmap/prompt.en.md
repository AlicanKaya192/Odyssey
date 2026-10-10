`corr_heatmap(columns)` should compute the correlation matrix of the columns in
the name → values dictionary (`np.corrcoef(list(columns.values()))`) and draw
it as a heat map with `imshow`: a two-sided colour scale `cmap="RdBu_r"` and
**symmetric** limits `vmin=-1, vmax=1`. Save it as `heat.png` and close the
figure. Return `[limits, matrix]`: the limits are `image.get_clim()` (two
`float`s), the matrix a list of lists rounded to 2 places. In the starter
code no limits are given, so the scale sits on the matrix's own minimum and
maximum.

**Expected output:**

```
[-1.0, 1.0]
[1.0, 0.85, -0.8]
[0.85, 1.0, -0.53]
[-0.8, -0.53, 1.0]
```
