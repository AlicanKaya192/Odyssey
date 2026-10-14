`alpha_bars(T, start, end, ts)` should build a linear noise schedule of `T`
steps (`np.linspace(start, end, T)`), compute `alpha = 1 - beta` and
`alpha_bar = np.cumprod(alpha)`, and return the `alpha_bar` values of the
steps in `ts` as a list of `float`s rounded to 4 places.

**Expected output:**

```
[0.9999, 0.9545, 0.6399, 0.0056]
[0.9999, 0.0786, 0.0]
```
