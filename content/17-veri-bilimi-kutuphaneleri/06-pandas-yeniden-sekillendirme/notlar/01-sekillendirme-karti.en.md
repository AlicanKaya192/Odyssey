## Wide to long

| Code | What it does |
|---|---|
| `df.melt(id_vars="city", var_name="month", value_name="sales")` | melts columns into rows |
| `df.melt(id_vars=..., value_vars=["jan", "feb"])` | only some columns |
| `df.stack()` | moves columns into the index's inner level |
| `pd.wide_to_long(df, stubnames="score", i="id", j="year", sep="_")` | from names like `score_2024` |
| `df.explode("tags")` | makes each list item a row |

## Long to wide

| Code | What it does |
|---|---|
| `df.pivot(index=, columns=, values=)` | rearranges; fails on a repeated pair |
| `df.pivot_table(..., aggfunc="sum")` | combines repeats with a calculation |
| `pivot_table(..., fill_value=0)` | fills empty cells |
| `pivot_table(..., margins=True)` | row and column totals |
| `pd.crosstab(a, b)` | counts of appearing together |
| `s.unstack()` | turns the inner level into columns |
| `s.unstack(fill_value=0)` | while filling empty cells |

## Afterwards

| Code | What it does |
|---|---|
| `wide[["jan", "feb"]]` | a natural order for the columns |
| `wide.reset_index().rename_axis(columns=None)` | back to a flat table |
| `long.dropna()` | drops the missing values pandas 3 `stack` keeps |

## Errors

| Symptom | Cause |
|---|---|
| `Index contains duplicate entries, cannot reshape` | a repeated pair in `pivot` |
| pivot_table numbers smaller than expected | the default `aggfunc` is mean |
| Columns in `feb, jan` order | the result is sorted alphabetically |
| A name at the table's top left | the column axis name (`columns.name`) |
| An unexpected `nan` after stack | pandas 3 does not drop missing values |
| `loc` returns a series after explode | the index was copied |
