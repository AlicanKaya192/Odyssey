`daily_totals(days, amounts)` should build a series indexed by day
(`pd.Series(amounts, index=days)`). The same day can appear more than once;
combine the repeats with `groupby(level=0).sum()` and return a `{day: total}`
dictionary. **Do not write a loop**; `to_dict()` is enough.

**Expected output:**

```
{'mon': 40, 'tue': 21, 'wed': 5}
```
