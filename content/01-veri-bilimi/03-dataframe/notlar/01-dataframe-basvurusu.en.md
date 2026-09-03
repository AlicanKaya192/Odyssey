Everything assumes `import pandas as pd`, with `data` being a DataFrame.

## Creating

| Written as | What it does |
|---|---|
| `pd.DataFrame({"a": [1, 2], "b": [3, 4]})` | From a dictionary; keys become column names |
| `pd.DataFrame([{"a": 1}, {"a": 2}])` | From a list of dictionaries; each one a row |
| `pd.DataFrame(rows, columns=["a", "b"])` | From a list of lists |
| `pd.read_csv("file.csv")` | From a CSV file |
| `series.to_frame()` | A one-column table from a Series |

## A first look

| Written as | What it gives |
|---|---|
| `data.shape` | `(rows, columns)` |
| `len(data)` | The number of rows |
| `data.columns` | The column names |
| `data.index` | The row labels |
| `data.dtypes` | The type of each column |
| `data.head(5)` / `data.tail(5)` | The first / last rows |
| `data.info()` | Columns, types, non-null counts, memory — all at once |
| `data.describe()` | A summary of the numeric columns |
| `data.sample(3)` | Three random rows |

`info()` is the most useful call when you first open a dataset: it shows
missing values and wrong types on a single screen.

## Selecting columns

| Written as | What it returns |
|---|---|
| `data["score"]` | A **Series** |
| `data[["score"]]` | A one-column **DataFrame** |
| `data[["name", "score"]]` | A two-column DataFrame |
| `data.select_dtypes("number")` | Only the numeric columns |

## Adding and removing columns

| Written as | What it does |
|---|---|
| `data["new"] = data["a"] + data["b"]` | Adds a computed column |
| `data["const"] = 0` | Adds a column with a constant value |
| `data.drop(columns=["a"])` | A **new table** with the column removed |
| `data.rename(columns={"a": "b"})` | A new table with the column renamed |
| `data.columns = ["x", "y"]` | Replaces all the names (in place) |

## Row operations

| Written as | What it does |
|---|---|
| `data.sort_values("score")` | A new table sorted by a column |
| `data.sort_values("score", ascending=False)` | Largest first |
| `data.sort_values(["city", "score"])` | By city, then by score |
| `data.drop_duplicates()` | Removes repeated rows |
| `data.reset_index(drop=True)` | Renumbers the index from zero |
| `data.set_index("name")` | Makes a column the index |

## The index

| Written as | What it does |
|---|---|
| `data.set_index("name")` | The `name` column becomes the index |
| `data.reset_index()` | The index becomes a column again |
| `data.reset_index(drop=True)` | The index is thrown away and renumbered |
| `data.index.name` | The name of the index |

The index is the name of the rows. It is what carries their identity through
sorting, filtering and joining.

## Aggregation

| Written as | What it gives |
|---|---|
| `data["score"].mean()` | The mean of one column |
| `data.mean(numeric_only=True)` | The mean of every numeric column |
| `data.sum(numeric_only=True)` | The totals |
| `data["score"].max()` | The largest value |
| `data["score"].idxmax()` | The **row label** of the largest |
| `data.loc[data["score"].idxmax()]` | The **whole row** with the highest score |
| `data.count()` | Non-empty cells per column |
| `data.nunique()` | Distinct values per column |

The last two are the quick way to see missing data and categorical columns.

## Missing values

| Written as | What it does |
|---|---|
| `data.isna()` | `True`/`False` cell by cell |
| `data.isna().sum()` | How many are missing **per column** |
| `data.dropna()` | Drops rows containing a gap |
| `data.dropna(subset=["score"])` | Drops based on that column only |
| `data.fillna(0)` | Fills every gap |
| `data.fillna({"score": 0})` | Fills with a different value per column |

`data.isna().sum()` is the second call you write when you open a dataset — it
shows at a glance how many gaps each column has.

## Converting types

| Written as | What it does |
|---|---|
| `data["a"].astype(int)` | To integer (**truncates**, does not round) |
| `data["a"].astype(float)` | To decimal |
| `data["a"].astype(str)` | To text |
| `pd.to_numeric(data["a"], errors="coerce")` | Turns unconvertible values into `NaN` |
| `pd.to_datetime(data["date"])` | To a date |

`to_numeric` is a lifesaver on messy numeric columns from a CSV: instead of
blowing up it turns the broken values into `NaN`, and then you can count
them.

## Saving

| Written as | What it does |
|---|---|
| `data.to_csv("out.csv", index=False)` | Writes to CSV |
| `data.to_dict("records")` | Converts to a list of dictionaries |
| `data.values` | Converts to a NumPy array |

Without `index=False` an index column is written into the file, and when you
read it back you get a column called `Unnamed: 0`.
