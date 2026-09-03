The whole module on one page. Assuming `import numpy as np`,
`import pandas as pd` and a table called `data`.

## NumPy

| Written as | What it does |
|---|---|
| `np.array([1, 2, 3])` | An array from a list |
| `np.arange(0, 10, 2)` | Generates by step |
| `np.linspace(0, 1, 5)` | Generates by number of pieces |
| `a.shape` / `a.dtype` / `a.size` | Shape, type, element count |
| `a.reshape(2, 3)` | The same data in a different layout |
| `a * 2`, `a + b` | Vectorised operations — no loop |
| `a[a > 70]` | Conditional selection |
| `a.sum()` / `.mean()` / `.std()` | Aggregation |
| `a.sum(axis=0)` | Down the columns |
| `np.nanmean(a)` | The mean, skipping missing values |

A slice is **not a copy**: change `a[1:3]` and the original array changes
too. For a copy, `.copy()`.

## Series

| Written as | What it does |
|---|---|
| `pd.Series([1, 2], index=["a", "b"])` | A labelled Series |
| `s["a"]` / `s.iloc[0]` | By label / by position |
| `s[s > 80]` | By condition |
| `s.value_counts()` | How many of each value |
| `s.unique()` / `s.nunique()` | Distinct values / their count |
| `s.isna().sum()` | How many blanks |
| `s.fillna(0)` / `s.dropna()` | Fill / drop |
| `s.str.strip()` / `s.str.lower()` | Text operations |
| `s.apply(function)` | To each element |

When two Series are added they **align on the labels**, not on position.

## DataFrame

| Written as | What it does |
|---|---|
| `pd.DataFrame({...})` | A table from a dict |
| `pd.read_csv("file.csv")` | From a file |
| `data.shape` / `data.columns` / `data.dtypes` | The structure |
| `data.head()` / `data.tail()` / `data.sample()` | A look |
| `data.describe()` | A numeric summary |
| `data["a"]` | One column (a Series) |
| `data[["a", "b"]]` | Several columns (a table) |
| `data["new"] = ...` | A new column |
| `data.drop(columns=["a"])` | Drops a column |
| `data.rename(columns={"a": "b"})` | Renames |
| `data.to_csv("out.csv", index=False)` | Saves |

## Selecting and filtering

| Written as | What it selects |
|---|---|
| `data.loc[0, "score"]` | Row and column by label |
| `data.iloc[0, 2]` | By position |
| `data.loc[data["score"] > 80]` | By condition |
| `data[(data["a"] > 1) & (data["b"] < 5)]` | Two conditions — **brackets required** |
| `data[data["city"].isin(["Ankara"])]` | Members of a list |
| `data[data["city"].str.contains("An")]` | Contains text |
| `data.sort_values("score", ascending=False)` | Sorts |
| `data.nlargest(3, "score")` | The three largest |

`and`/`or` do not work; you use `&` and `|`, with each condition in
brackets.

## Grouping

| Written as | What it gives |
|---|---|
| `data.groupby("c")["s"].mean()` | The group average |
| `data.groupby("c")["s"].agg(["count", "mean"])` | **The right way** |
| `data.groupby(["c1", "c2"])["s"].mean()` | Two breakdowns |
| `data.groupby("c").size()` | The group sizes |
| `data.groupby("c")["s"].transform("mean")` | Each row's own group average |
| `data.pivot_table(values="s", index="c1", columns="c2")` | A summary table |
| `pd.crosstab(data["c1"], data["c2"])` | A cross count |

## Cleaning

| Written as | What it does |
|---|---|
| `data.columns.str.strip().str.lower()` | Column names |
| `data["c"].str.strip().str.title()` | Text consistency |
| `pd.to_numeric(data["c"], errors="coerce")` | To numbers, the rest to `NaN` |
| `data.duplicated().sum()` | How many duplicates |
| `data.drop_duplicates(subset=["id"])` | Drops duplicates |
| `data.dropna(subset=["score"])` | Drops rows blank in one column |
| `data["c"].fillna(data["c"].median())` | Fills with the median |
| `data["c"].replace(999, None)` | Turns a hidden code into a blank |

The order: **names → text → types → duplicates → gaps.**

## Visualisation

| Written as | What it draws |
|---|---|
| `fig, ax = plt.subplots()` | A canvas and a drawing area |
| `ax.bar(x, y)` / `ax.barh(x, y)` | Vertical / horizontal bars |
| `ax.plot(x, y, marker="o")` | A line |
| `ax.scatter(x, y)` | A scatter plot |
| `ax.hist(values, bins=10)` | A histogram |
| `ax.set_title(...)` / `set_xlabel` / `set_ylabel` | Labels — **required** |
| `ax.set_ylim(0, 100)` | The axis range |
| `fig.savefig("c.png", dpi=150, bbox_inches="tight")` | Saves |
| `plt.close(fig)` | Closes the canvas |

Inside Odyssey the `matplotlib.use("Agg")` line is needed.

| What you are showing | Which chart |
|---|---|
| Comparing categories | Bars |
| Change over time | A line |
| The distribution of a column | A histogram |
| The relationship between two columns | A scatter plot |

## The exploration order

1. `data.shape` — the scale
2. `data.dtypes` — are the types right
3. `data.head()` — what is in there
4. `data.isna().sum()` — the gaps
5. `data.describe()` — mean, median, extremes
6. `data["c"].value_counts()` — are the categories balanced
7. `data.groupby(...).agg(["count", "mean"])` — do the groups differ
8. `data.corr(numeric_only=True)` — do the columns move together

## Outliers

```python
q1 = data["score"].quantile(0.25)
q3 = data["score"].quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

outliers = data[(data["score"] < low) | (data["score"] > high)]
```

## Rules to remember

- pandas methods **return a new object**; store the result in a variable.
- Write with `loc` in one step instead of chained assignment.
- A group average is not read without `count`.
- Correlation is not causation.
- A bar chart axis starts at zero.
- The raw data is preserved and you work on a copy.
