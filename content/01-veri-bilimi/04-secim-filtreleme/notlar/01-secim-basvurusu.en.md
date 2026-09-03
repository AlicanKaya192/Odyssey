`data` is a DataFrame, `s` a Series.

## iloc — by position

| Written as | What it selects |
|---|---|
| `data.iloc[0]` | The first row (as a Series) |
| `data.iloc[-1]` | The last row |
| `data.iloc[0, 2]` | The third column of the first row |
| `data.iloc[1:3]` | Rows 1 and 2 — **end excluded** |
| `data.iloc[:, 0]` | The whole first column |
| `data.iloc[:, [0, 2]]` | The first and third columns |
| `data.iloc[[0, 3], [1, 2]]` | Chosen rows and columns |
| `data.iloc[:5]` | The first five rows |

## loc — by label

| Written as | What it selects |
|---|---|
| `data.loc[0]` | The row **labelled** `0` |
| `data.loc["Mina"]` | The row labelled `Mina` |
| `data.loc["Mina", "score"]` | A single cell |
| `data.loc["Ada":"Mina"]` | A label range — **end included** |
| `data.loc[:, "score"]` | A whole column |
| `data.loc[:, "name":"score"]` | A column range, end included |
| `data.loc[mask]` | The rows matching a condition |
| `data.loc[mask, "score"]` | One column of the matching rows |

**The slicing difference:** `iloc[1:3]` gives two rows, `loc["a":"c"]` gives
three.

## Filtering by condition

| Written as | What it does |
|---|---|
| `data[data["score"] > 80]` | The matching rows |
| `data[(a) & (b)]` | Two conditions together |
| `data[(a) \| (b)]` | Either one |
| `data[~(a)]` | The opposite of a condition |
| `data[data["city"].isin([...])]` | One of the listed values |
| `data[data["age"].between(20, 30)]` | A range — **both ends included** |
| `data[data["name"].str.contains("An")]` | Searching in text |
| `data[data["name"].str.startswith("A")]` | Matching from the start |
| `data[data["score"].isna()]` | The missing ones |
| `data[data["score"].notna()]` | The filled ones |

`and`, `or` and `not` **do not work**; use `&`, `|` and `~`, with each
condition in parentheses.

## query

| Written as | What it does |
|---|---|
| `data.query("score > 80")` | A single condition |
| `data.query("score > 80 and city == 'Ankara'")` | `and` works here |
| `data.query("city in ['Ankara', 'Izmir']")` | The equivalent of `isin` |
| `data.query("score > @limit")` | Use an outside variable with `@` |

Column names go without quotes, text values in single quotes. If a column
name has a space, use backticks: ``data.query("`my col` > 5")``.

## Selection based on order

| Written as | What it gives |
|---|---|
| `data.nlargest(3, "score")` | The three largest rows |
| `data.nsmallest(3, "score")` | The three smallest rows |
| `data.sort_values("score").head(3)` | The same, in two steps |
| `data.loc[data["score"].idxmax()]` | The **row** of the largest |
| `data.sample(3)` | Three random rows |

`nlargest` does not sort everything, it just finds the largest; noticeably
faster on large data.

## Changing values

| Written as | What it does |
|---|---|
| `data.loc[mask, "score"] = 0` | Changes one column of the matching rows |
| `data.loc[mask, ["a", "b"]] = 0` | Several columns |
| `data["score"] = data["score"].clip(0, 100)` | Trims anything outside the bounds |
| `data["city"] = data["city"].replace({"izmir": "Izmir"})` | Fixes values |
| `data.loc[:, "score"] = 0` | The whole column |

**Always a single `loc` call.** `data[mask]["score"] = 0` silently does
nothing.

## Dropping rows and columns

| Written as | What it does |
|---|---|
| `data.drop(columns=["a"])` | Drops a column |
| `data.drop(index=[0, 2])` | Drops the rows with those labels |
| `data[data["score"].notna()]` | Drops the missing ones (by filtering) |
| `data.dropna(subset=["score"])` | The same, with a built-in method |
| `data.drop_duplicates()` | Drops repeated rows |

## Common combinations

```python
# The name of the highest scorer in one city
selected = data[data["city"] == "Ankara"]
print(selected.loc[selected["score"].idxmax(), "name"])

# The mean of the rows matching two conditions
mask = (data["score"] >= 70) & (data["age"] < 25)
print(data.loc[mask, "score"].mean())

# How many rows match a condition
print((data["score"] >= 80).sum())
```

The trick on the last line: a mask is a Series of `True`/`False` and `sum()`
counts them — the shortest way to learn how many there are without
filtering.
