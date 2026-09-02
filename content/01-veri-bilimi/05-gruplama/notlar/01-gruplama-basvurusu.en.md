# Grouping Reference

`data` is a DataFrame.

## Basic grouping

| Written as | What it gives |
|---|---|
| `data.groupby("city")["score"].mean()` | The mean per city — a Series |
| `data.groupby("city")["score"].sum()` | The total |
| `data.groupby("city")["score"].count()` | The number of **filled** cells |
| `data.groupby("city").size()` | The number of **all** rows |
| `data.groupby("city")["score"].min()` / `.max()` | The extremes |
| `data.groupby("city")["score"].median()` | The median |
| `data.groupby("city")["score"].std()` | The standard deviation |
| `data.groupby("city")["name"].nunique()` | Distinct values per group |
| `data.groupby("city")["score"].first()` / `.last()` | The first / last row |

Groups come out **sorted alphabetically**. You can pass `sort=False` to skip
that; on large data it is slightly faster.

## Several calculations

| Written as | What it gives |
|---|---|
| `.agg(["count", "mean", "max"])` | A three-column table |
| `.agg(people=("name", "count"), avg=("score", "mean"))` | Named columns |
| `.agg({"score": "mean", "age": "max"})` | A different calculation per column |
| `.describe()` | Eight numbers per group |

The named form (`new_name=("column", "calculation")`) reads best when
producing a report.

## Several keys

| Written as | What it gives |
|---|---|
| `data.groupby(["city", "grade"])["score"].mean()` | A MultiIndex |
| `... .reset_index()` | Turns the levels into columns |
| `... .unstack()` | Makes the second key into columns (like a pivot) |
| `data.groupby("city", as_index=False)` | The key stays a column |

## Pivot table

| Written as | What it does |
|---|---|
| `pivot_table(index="city", columns="grade", values="score")` | Default calculation: the mean |
| `..., aggfunc="sum"` | Changes the calculation |
| `..., aggfunc=["mean", "count"]` | Several calculations |
| `..., fill_value=0` | Fills the empty cells |
| `..., margins=True` | Adds row and column totals |

`pivot_table` and `groupby(...).unstack()` give the same result; the first
reads better.

## Working with the group result

The result is a Series or a table; everything you learned about Series
applies.

| Written as | What it does |
|---|---|
| `.sort_values(ascending=False)` | Sorts largest first |
| `.idxmax()` | The **name of the group** with the highest value |
| `.head(3)` | The first three groups |
| `.round(2)` | Rounds |
| `.to_dict()` | Converts to a dictionary |
| `.reset_index()` | Converts to an ordinary table |

## transform and filter

| Written as | What it does |
|---|---|
| `data.groupby("city")["score"].transform("mean")` | Writes the group mean onto **every row** |
| `data.groupby("city")["score"].transform("rank")` | The rank within the group |
| `data.groupby("city").filter(lambda g: len(g) > 2)` | Only the rows of the larger groups |

`transform` keeps the table the **same size**; `agg` shrinks it. If you are
going to compare a row with its group's mean, you need `transform`.

## Counting patterns

```python
# How many of each category
data["city"].value_counts()

# The same with groupby
data.groupby("city").size()

# The intersection of two categories
data.groupby(["city", "grade"]).size()

# Percentage per category
data["city"].value_counts(normalize=True) * 100
```

`value_counts()` is shorter for a single column; `groupby` is for when you
need other calculations too.

## Common patterns

```python
# The city with the highest average
data.groupby("city")["score"].mean().idxmax()

# The best person in each group
data.loc[data.groupby("city")["score"].idxmax()]

# Everyone above their group's mean
mean_by_city = data.groupby("city")["score"].transform("mean")
data[data["score"] > mean_by_city]

# A report table
data.groupby("city").agg(
    people=("name", "count"),
    average=("score", "mean"),
    highest=("score", "max"),
).round(1).sort_values("average", ascending=False)
```

The second pattern works because `idxmax()` gives one **row label** per
group and `loc` fetches those whole rows.

## Missing values

| Situation | Behaviour |
|---|---|
| The key column is missing | The row **joins no group** and drops out silently |
| `dropna=False` | The missing key becomes a group called `NaN` |
| The computed column is missing | `mean` and `sum` skip it, `count` does not count it |

Running `isna().sum()` on the key column before grouping is a good habit —
otherwise you spend a long time looking for why the totals do not add up.
