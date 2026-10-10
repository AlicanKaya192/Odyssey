## .str

| Code | What it does |
|---|---|
| `s.str.strip()` / `.lower()` / `.title()` | cleaning spaces and case |
| `s.str.len()` | length (decimal if missing values) |
| <code>s.str.contains("a&#124;b", case=False, na=False)</code> | is the pattern there |
| `s.str.contains(".", regex=False)` | a plain text search |
| `s.str.startswith("TR")` | the start |
| `s.str.replace(r"\d", "#", regex=True)` | replacing by pattern |
| `s.str.extract(r"(?P<name>...)")` | opens the groups into columns |
| `s.str.split("-", expand=True)` | opens the parts into columns |
| `s.str[:2]` | a slice |

## category

| Code | What it does |
|---|---|
| `s.astype("category")` | turns into a category |
| `s.cat.categories` / `s.cat.codes` | the value list / the row codes |
| `pd.CategoricalDtype([...], ordered=True)` | you give the order |
| `s.cat.remove_unused_categories()` | drops the unused ones |
| `groupby(..., observed=False)` | shows empty categories too |
| `pd.cut(s, bins=[...], labels=[...])` | classes by your limits |
| `pd.qcut(s, q=4)` | split into equally sized groups |

## Errors

| Symptom | Cause |
|---|---|
| The same city counted several times | spaces or case; `strip`, `lower` |
| `Cannot mask with non-boolean array` | a missing value in `object` type; `na=False` |
| `.` found everything | the pattern is a regex; `regex=False` |
| Sizes in `L, M, S, XL` order | text sorting; an ordered category |
| `NaN` after `cut` | the value is outside the limits |
| A category with no rows in a report | the category list is apart from the data |
| The category saved no memory | too many different values |
