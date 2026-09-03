## Exploring

| Written as | What it shows |
|---|---|
| `data.shape` | How many rows and columns |
| `data.info()` | Columns, types, non-null counts — on one screen |
| `data.dtypes` | The column types |
| `data.head()` / `data.sample(5)` | A first look at the data |
| `data.isna().sum()` | Missing count per column |
| `data.duplicated().sum()` | How many duplicated rows |
| `data.nunique()` | Distinct values per column |
| `data.describe()` | A numeric summary |
| `data.describe(include="all")` | Including the text columns |

`info()` and `isna().sum()` are the first two things you write when you open
a dataset.

## Column names

| Written as | What it does |
|---|---|
| `data.columns = data.columns.str.strip()` | Removes leading/trailing spaces |
| `data.columns = data.columns.str.lower()` | Lowercases them |
| `data.columns = data.columns.str.replace(" ", "_")` | Spaces become underscores |
| `data.rename(columns={"old": "new"})` | Renames them one by one |
| `data.columns.duplicated().any()` | Are there columns with the same name |

They chain: `data.columns.str.strip().str.lower()`.

## Cleaning text

| Written as | What it does |
|---|---|
| `s.str.strip()` | Leading and trailing spaces |
| `s.str.lower()` / `s.str.upper()` / `s.str.title()` | Case |
| `s.str.replace("-", " ")` | Replaces |
| `s.str.replace(r"\s+", " ", regex=True)` | Collapses repeated spaces |
| `s.str.contains("An")` | Whether it contains something |
| `s.str.startswith("A")` | Matching from the start |
| `s.str.len()` | The length |
| `s.str.split(",")` | Splits |
| `s.str.extract(r"(\d+)")` | Pulls out the part matching a pattern |

None of these work without `.str`. They leave missing values alone.

## Converting types

| Written as | What it does |
|---|---|
| `pd.to_numeric(s, errors="coerce")` | Turns what it cannot convert into `NaN` |
| `pd.to_datetime(s, errors="coerce")` | Converts to a date |
| `s.astype(int)` | **Truncates** to integer — fails if there are gaps |
| `s.astype(float)` | Converts to decimal |
| `s.astype(str)` | Converts to text |
| `s.round(2).astype(int)` | Round first, then convert |

`errors="coerce"` is the most-used argument in cleaning work: it marks the
broken values without stopping the program.

## Missing values

| Written as | What it does |
|---|---|
| `data.isna().sum()` | Count per column |
| `data.isna().sum().sum()` | Across the whole table |
| `data.isna().mean()` | The **proportion** per column |
| `data.dropna()` | Drops rows where any column is empty |
| `data.dropna(subset=["score"])` | Looks only at that column |
| `data.dropna(axis=1)` | Drops **columns** containing gaps |
| `data.dropna(thresh=3)` | Keeps rows with at least three filled cells |
| `data.fillna(0)` | Fills everything |
| `data.fillna({"score": 0, "city": "Unknown"})` | A different value per column |
| `s.fillna(s.mean())` | With the mean |
| `s.fillna(s.median())` | With the median — safer when there are extremes |
| `s.ffill()` / `s.bfill()` | With the value above / below |

`isna().mean()` gives a proportion, which makes deciding easier: 2% missing
makes dropping reasonable, 60% missing means questioning the column
entirely.

## Duplicated rows

| Written as | What it does |
|---|---|
| `data.duplicated()` | Marks the second and later copies |
| `data.duplicated().sum()` | How many |
| `data.duplicated(subset=["id"])` | Looks only at that column |
| `data.drop_duplicates()` | Keeps the first |
| `data.drop_duplicates(keep="last")` | Keeps the last |
| `data.drop_duplicates(subset=["id"], keep="last")` | By identity, keeping the newest |
| `data[data.duplicated(keep=False)]` | Shows **all** the duplicates |

That last line is for inspecting: looking at which records repeat before
deleting them is a good habit.

## Fixing values

| Written as | What it does |
|---|---|
| `s.replace({"yes": 1, "no": 0})` | Replaces using a dictionary |
| `s.replace(-1, np.nan)` | Turns fake missing values into real `NaN` |
| `s.map({"a": 1, "b": 2})` | Replaces; anything unmatched becomes `NaN` |
| `s.clip(0, 100)` | Trims anything outside the bounds |
| `data.loc[mask, "column"] = value` | Assignment by condition |

Values like `-1`, `999` or `"unknown"` usually mean "missing". Turning them
into real `NaN` is one of the first jobs — otherwise they get mixed into the
averages.

## Outliers

```python
q1 = s.quantile(0.25)
q3 = s.quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

outliers = s[(s < low) | (s > high)]
clean = s[(s >= low) & (s <= high)]
```

| Approach | When |
|---|---|
| IQR (above) | General purpose, no assumption about the distribution |
| `s.clip(low, high)` | Pulling the value to the bound without losing the record |
| Manual bounds | When you have domain knowledge (a score is 0-100, an age 0-120) |

Before deleting an outlier you have to **ask why it is there**: is it a real
extreme value or a data-entry mistake?

## Saving

| Written as | What it does |
|---|---|
| `data.to_csv("clean.csv", index=False)` | The clean version to a separate file |
| `raw.copy()` | Working without damaging the raw data |

**Never write over the raw file.** You discover a mistake in your cleaning
steps days later.
