Assuming `import pandas as pd` and a table called `data`.

## The order

| Step | Call | What it asks |
|---|---|---|
| 1 | `data.shape` | How many rows, how many columns |
| 2 | `data.dtypes` | Is every column the expected type |
| 3 | `data.head()` | What is actually in there |
| 4 | `data.isna().sum()` | Where the gaps are |
| 5 | `data.describe()` | A summary of the numeric columns |
| 6 | `data["col"].value_counts()` | Are the categories balanced |
| 7 | `data.groupby(...)` | Do the groups differ |
| 8 | `data.corr()` | Do the columns move together |

## First look

| Written as | What it gives |
|---|---|
| `data.shape` | A `(rows, columns)` tuple |
| `data.columns.tolist()` | The column names |
| `data.dtypes.astype(str).tolist()` | The types, as a readable list |
| `data.head(5)` / `data.tail(5)` | The first / last five rows |
| `data.sample(5)` | Five random rows |
| `len(data)` | The row count |

`sample()` is a more honest look than `head()`: if the data is sorted by
date, the first five rows show you only the oldest records.

## Missing values

| Written as | What it gives |
|---|---|
| `data.isna().sum()` | The count of blanks per column |
| `data.isna().sum().sum()` | The total number of blanks |
| `data.isna().any(axis=1).sum()` | The number of rows with at least one blank |
| `(data.isna().mean() * 100).round(1)` | The percentage of blanks per column |
| `data.dropna(subset=["score"])` | Drop rows blank in a particular column |

A percentage says more than a count: 20 blanks in 100 rows is not the same
thing as 20 blanks in 100,000.

## Numeric summary

| Written as | What it gives |
|---|---|
| `data.describe()` | An eight-row summary table |
| `data["s"].mean()` / `.median()` | The mean / the median |
| `data["s"].std()` | The standard deviation |
| `data["s"].quantile(0.25)` | The first quartile |
| `data["s"].min()` / `.max()` | The extremes |
| `data["s"].idxmax()` | The **label** of the largest |
| `data["s"].skew()` | Skew; 0 is symmetric |

Reading `describe()`:

| What you see | What it means |
|---|---|
| `mean` far from `50%` | The distribution is skewed, there are extremes |
| Small `std` | The values are close together |
| Large `std` | A wide spread; there may be two different groups |
| A nonsensical `min` or `max` | A data error, or a different unit |
| `count` below the row count | That column has missing values |

## Categorical summary

| Written as | What it gives |
|---|---|
| `data["c"].value_counts()` | How many of each value |
| `data["c"].value_counts(normalize=True)` | As a proportion |
| `data["c"].nunique()` | How many distinct values |
| `data["c"].unique()` | The values themselves |
| `data["c"].value_counts().head(10)` | The ten most frequent values |

If `nunique()` equals the row count, that column is an id column; it is of
no use for grouping.

## Groups

| Written as | What it gives |
|---|---|
| `data.groupby("c")["s"].mean()` | Group averages |
| `data.groupby("c")["s"].agg(["count", "mean"])` | **Together** — the right way |
| `data.groupby("c")["s"].agg(["count", "mean", "std"])` | With the spread |
| `data.groupby(["c1", "c2"])["s"].mean()` | Two breakdowns |
| `data.groupby("c")["s"].median()` | When there are outliers |

**An average is not read without `count`.** Without knowing how many people
it was computed from, an average is not information.

## Relationships

| Written as | What it gives |
|---|---|
| `data["a"].corr(data["b"])` | A single number between two columns |
| `data.corr(numeric_only=True)` | A matrix of all the numeric columns |
| `data.corr(numeric_only=True).round(2)` | The readable form |
| `data.plot(kind="scatter", x="a", y="b")` | Looking with your eyes |

A rough scale for reading a correlation:

| Value | Reading |
|---|---|
| 0.0 - 0.3 | Weak or none |
| 0.3 - 0.7 | Moderate |
| 0.7 - 1.0 | Strong |

The sign gives the direction: `-0.8` is strong too, in the other direction.

**Look at a scatter plot before you look at the correlation.** If the
relationship is curved, the correlation can come out at 0 and you conclude
there is no relationship.

## Outliers

```python
q1 = data["score"].quantile(0.25)
q3 = data["score"].quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

outliers = data[(data["score"] < low) | (data["score"] > high)]
```

| Written as | What it does |
|---|---|
| `data["s"].quantile(0.25)` | The first quartile |
| `data["s"].nlargest(5)` | The five largest |
| `data["s"].nsmallest(5)` | The five smallest |
| `ax.boxplot(data["s"])` | A box plot — it shows the outliers |

`nlargest` is the quickest way to spot an outlier by eye: if the extreme
values are detached from the rest, you notice.

## Breakdown tables

| Written as | What it gives |
|---|---|
| `pd.crosstab(data["c1"], data["c2"])` | A cross count of two categories |
| `pd.cut(data["age"], bins=[20, 30, 40, 60])` | Turns a number into a range |
| `data.pivot_table(values="s", index="c1", columns="c2")` | A summary table |

`pd.cut` turns a continuous column into a category; grouping by age band
rather than age is usually more readable.

## Checklist

- [ ] How many rows, how many columns?
- [ ] Are the types right?
- [ ] Are there missing values, and what percentage?
- [ ] Are the mean and the median far apart in `describe`?
- [ ] Do `min`/`max` make sense?
- [ ] Are the categories balanced?
- [ ] Is there a difference between the groups — and how big are they?
- [ ] Do the columns move together?
- [ ] Are there outliers, and what caused them?
- [ ] How would I write the finding in one sentence?
