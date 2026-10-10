A category's list of values lives **apart from the data**. So a category
with no rows at all (no XL was ever sold) keeps existing in the table.
Sometimes that is what you want (the report should show "XL: 0"), sometimes
it is confusing.

```python
import pandas as pd

size_type = pd.CategoricalDtype(["S", "M", "L", "XL"], ordered=True)
sizes = pd.Series(["M", "S", "M"], dtype=size_type)
df = pd.DataFrame({"size": sizes, "qty": [2, 1, 4]})
print(df.groupby("size")["qty"].sum().to_dict())
print(df.groupby("size", observed=False)["qty"].sum().to_dict())
print(df["size"].value_counts().to_dict())
small = df[df["size"] != "M"]
print(small["size"].cat.categories.tolist())
print(small["size"].cat.remove_unused_categories().cat.categories.tolist())
```

```text
{'S': 1, 'M': 6}
{'S': 1, 'M': 6, 'L': 0, 'XL': 0}
{'M': 2, 'S': 1, 'L': 0, 'XL': 0}
['S', 'M', 'L', 'XL']
['S']
```

## What happened?

- In pandas 3, `groupby` gives only the **observed** categories by default
  (`observed=True`): S and M.
- `observed=False` gives all categories and writes 0 for those with no rows.
  Use it if you want "a size never sold" to show in the report too.
- `value_counts`, however, always counts every category; the unsold ones are
  0. The same column can give results of two different lengths in two
  different functions.
- Filtering does not delete categories: the M rows are gone but `M` is still
  in the categories. `remove_unused_categories()` keeps only the used ones.

## Why does it matter?

Empty bars in a chart, a column opened for a never-seen class in a model (in
one-hot encoding) or a longer-than-expected result list all come from the
same cause: the category list holds more than what is in the data. When
working with a categorical column, "what is in the list" (`cat.categories`)
and "what is in the data" (`unique()`) are separate questions.
