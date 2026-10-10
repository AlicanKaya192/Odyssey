In `monthly_sum(records)` the same pair can appear more than once in the
`[city, month, sales]` records; that is why the starter code's `pivot`
fails. It should total with `pivot_table` (`aggfunc="sum"`), a cell with no
records should be 0 (`fill_value=0`), and return the result as a `{city:
{month: total}}` dictionary (`to_dict(orient="index")`). **Do not write a
loop.**

**Expected output:**

```
{'feb': 0, 'jan': 80}
{'feb': 65, 'jan': 0}
```
