`values` in `missing_and_mean(values)` may contain `None`. Turn the list
into a decimal array with `np.array(values, dtype=float)` (`None` → `nan`)
and return the missing count (`np.isnan(...).sum()`) and the mean without the
missing values (`np.nanmean`, rounded to 2 places) as `[missing, mean]`.

**Expected output:**

```
[1, 4.0]
[0, 2.0]
```
