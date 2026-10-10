## Index

| Code | What it does |
|---|---|
| `df.set_index("a")` | moves a column into the index |
| `df.set_index(["a", "b"])` | a two-level MultiIndex |
| `df.reset_index()` | turns the index back into columns |
| `df.loc[label]` / `df.iloc[position]` | select by label / by position |
| `s1.add(s2, fill_value=0)` | adds, counting the missing side as 0 |
| `s.reindex(list)` | puts labels in the given order, `NaN` for missing |
| `idx.is_unique` / `idx.duplicated()` | checks for repeats |
| `set_index(..., verify_integrity=True)` | fails if there are repeats |
| `df.sort_index()` | sorts by the index |

## MultiIndex

| Code | What it does |
|---|---|
| `m.loc[("Izmir", 2025)]` | a full label (tuple) |
| `m.loc["Izmir"]` | the outer level; that level is dropped |
| `m.xs(2025, level="year")` | select from an inner level |
| `m.loc[pd.IndexSlice["A":"B", 2024], :]` | a slice on two levels |
| `m.index.get_level_values("city")` | one level's labels |
| `m.swaplevel()` | swaps the levels |
| `m.droplevel("year")` | drops a level |
| `g.unstack()` | turns the inner level into columns |
| `g.groupby(level="city").sum()` | totals over one level |

## Errors

| Symptom | Cause |
|---|---|
| An unexpected `NaN` in a sum | the labels do not match (alignment) |
| Integers became `float64` | the `NaN` from alignment |
| A wrong total with `.values` | labels dropped, added by order |
| `loc` sometimes returns a series | a repeated label |
| `cannot reindex on an axis with duplicate labels` | a repeated label |
| `UnsortedIndexError ... lexsort depth` | no `sort_index()` before slicing |
| `KeyError` on an inner-level value | `loc` looks at the outer level; use `xs` |
