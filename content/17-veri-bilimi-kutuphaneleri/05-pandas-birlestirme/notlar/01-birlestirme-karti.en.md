## Which one?

| Want | Code |
|---|---|
| Match on a key column | `a.merge(b, on="key", how="left")` |
| Key names differ | `a.merge(b, left_on="x", right_on="y")` |
| Key is in the index | `a.join(b)` or `merge(..., left_index=True, right_index=True)` |
| Stack same-shaped pieces | `pd.concat(pieces, ignore_index=True)` |
| Keep each piece's source | `pd.concat(pieces, keys=names)` |
| Side by side (by index) | `pd.concat([a, b], axis=1)` |
| By the nearest time | `pd.merge_asof(a, b, on="time")` |

## how

| `how` | Kept |
|---|---|
| `inner` | keys on both sides (merge's default) |
| `left` | all of the left (join's default) |
| `right` | all of the right |
| `outer` | all of both |
| `cross` | every row with every row (no key) |

## Checks

| Code | What it does |
|---|---|
| `indicator=True` | a `_merge` column: `both` / `left_only` / `right_only` |
| `validate="many_to_one"` | `MergeError` if a key repeats on the right |
| `len(result) == len(a)` | the row count must not change when adding information |
| `b["key"].is_unique` | is the key unique on the side being matched |
| `a["key"].dtype == b["key"].dtype` | are the key types equal |

## Errors

| Symptom | Cause |
|---|---|
| Rows vanished | the default `inner`; the unmatched dropped |
| Rows multiplied, the total grew | a repeated key on the right |
| `You are trying to merge on int64 and str columns` | different key types |
| `sales_x`, `sales_y` columns | a same-named column; give `suffixes` |
| An integer column became decimal | `NaN` in an unmatched row |
| `loc` returns a series after concat | a repeated index; `ignore_index=True` |
