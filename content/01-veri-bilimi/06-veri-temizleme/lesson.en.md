# Cleaning Data

In the first section we said: **most of the time goes into the two middle
boxes.** This section is the second of those boxes.

Real data does not arrive clean. Spaces in column names, three different
spellings of the same city, text in a column that should be numeric,
duplicated rows, empty cells. There is no such thing as clean data; there is
**data that has been cleaned**.

The examples in this section use this table — deliberately awful:

```python
raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", None],
    "score": ["82", "74", None, "82", "abc"],
})
```

Five rows with five separate problems. We will work through them in order.

## Look first, touch afterwards

```python
print(raw.shape)
print(list(raw.columns))
print(raw.dtypes)
print(raw.isna().sum())
```

```text
(5, 3)
[' Name ', 'city', 'score']
Name      str
city      str
score     str
dtype: object
 Name     0
city      1
score     1
dtype: int64
```

Two problems are visible at first glance: the column is called `" Name "`
(with spaces at both ends) and `score` is of type **text** where it should be
numeric.

`info()` gives the same information on one screen. It is the first thing you
write when you open a dataset.

## 1. Column names

```python
data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
print(list(data.columns))
```

```text
['name', 'city', 'score']
```

`" Name "` and `"name"` are two different names; both look the same on
screen, and writing `data["name"]` gives you a `KeyError` whose cause is
invisible.

That is why **cleaning the column names is the first job**: strip the spaces,
lowercase everything. After that you never have to think about how to spell
them.

## 2. Text columns

```python
data["name"] = data["name"].str.strip().str.title()
data["city"] = data["city"].str.strip().str.title()
print(data[["name", "city"]])
```

```text
    name    city
0    Ada  Ankara
1  Kerem   Izmir
2   Mina  Ankara
3    Ada  Ankara
4  Deniz     NaN
```

`"izmir "`, `"ANKARA"` and `"Ankara"` are now a single spelling. Group
without doing this and you get **three separate cities**.

- `str.strip()` removes leading and trailing spaces.
- `str.title()` capitalises the first letter of each word.
- `str.lower()` and `str.upper()` exist too; which you choose does not
  matter, **being consistent** does.

Missing values (`None`) are left alone — `str` methods do not touch them.

## 3. Fixing types

```python
data["score"] = pd.to_numeric(data["score"], errors="coerce")
print(data["score"].tolist())
print(data["score"].dtype)
```

```text
[82.0, 74.0, nan, 82.0, nan]
float64
```

`"abc"` could not be converted and became `NaN`. `errors="coerce"` says
exactly that: **do not blow up on what you cannot convert, leave it empty.**

Had you tried `astype(int)`, the whole program would have failed.
`to_numeric` confines the problem to a single cell, and you then decide what
to do about it.

Note that the result is `float64`: the integer type cannot hold `NaN`.

## 4. Missing values

```python
print(data.isna().sum())
```

```text
name     0
city     1
score    2
dtype: int64
```

There are now two missing scores — one was empty from the start and one was
created by `"abc"`.

You have three options and **none of them is always right**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Drop</span><span class="anat-body"><code>dropna()</code> — you lose the record entirely. Reasonable when there are few</span></div>
    <div class="anat-row"><span class="anat-label">Fill</span><span class="anat-body"><code>fillna(mean)</code> — the record stays, but with a made-up value</span></div>
    <div class="anat-row"><span class="anat-label">Leave</span><span class="anat-body">Calculations skip them anyway; but you need to know how many there are</span></div>
  </div>
</figure>

```python
print(data.dropna().shape)
print(data.dropna(subset=["score"]).shape)
print(data["score"].fillna(data["score"].mean()).round(1).tolist())
```

```text
(3, 3)
(3, 3)
[82.0, 74.0, 79.3, 82.0, 79.3]
```

`dropna()` drops a row if **any** column is empty — very aggressive.
`dropna(subset=["score"])` looks only at the column you care about; usually
that is what you want.

Filling with the mean does not change the mean but **reduces the spread**: it
makes the data look more consistent than it is. The decision is yours, and
you have to state it in your report.

## 5. Duplicated rows

```python
print(data.duplicated().sum())
print(data.drop_duplicates(subset=["name"]).shape)
```

```text
1
(4, 3)
```

`Ada` appears twice. `duplicated()` marks the **second and later** copies;
the first is kept.

Without `subset` every column has to match. In real data you usually look at
an identity column: if the same student number was entered twice, that is a
duplicate even if the scores differ.

`keep="last"` keeps the last record instead — useful when you want to keep
the updated one.

## 6. Outliers

```python
scores = pd.Series([10, 12, 11, 13, 100])
q1 = scores.quantile(0.25)
q3 = scores.quantile(0.75)
iqr = q3 - q1

print(q1, q3, iqr)
print(scores[(scores < q1 - 1.5 * iqr) | (scores > q3 + 1.5 * iqr)].tolist())
```

```text
11.0 13.0 2.0
[100]
```

**The IQR method:** anything more than 1.5 times the interquartile range away
counts as an outlier. A common, simple rule that is good enough most of the
time.

What do you do when you find one? **Ask why it is there first.** Is 100 a
real score, or was 10 typed with an extra zero? Deleting it without knowing
is prettifying the data, not cleaning it.

To bound the values there is `clip`:

```python
print(pd.Series([-5, 50, 150]).clip(0, 100).tolist())
```

```text
[0, 50, 100]
```

## In order

The order of the cleaning steps matters:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Look</b><br>shape, dtypes, isna</span>
    <span class="arrow">→</span>
    <span class="node"><b>Names</b><br>fix the column names</span>
    <span class="arrow">→</span>
    <span class="node"><b>Text</b><br>spaces and case</span>
    <span class="arrow">→</span>
    <span class="node"><b>Types</b><br>convert to numeric</span>
    <span class="arrow">→</span>
    <span class="node"><b>Duplicates</b><br>drop the copies</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Missing</b><br>decide</span>
  </div>
  <figcaption>Text is cleaned before types: the text " 82 " can still be converted, but inconsistent spellings cannot be fixed after a type conversion.</figcaption>
</figure>

Missing values come **last** for a reason: type conversion creates new gaps
(`"abc"` becomes `NaN`). Fill first and convert afterwards and you miss those
cells.

## Cleaning cannot be undone

All of these steps **change** the data. Working on a copy is a good habit so
you do not lose the raw version:

```python
data = raw.copy()
```

And never write over the file: save to a separate `clean.csv`. You discover a
mistake in your cleaning steps three days later and need to go back to the
raw data.

## Summary

- **Look first:** `shape`, `dtypes`, `isna().sum()`, `head()`.
- **Column names** are the first thing cleaned:
  `str.strip().str.lower()`.
- **In text columns**, inconsistent spaces and case break grouping.
- **`pd.to_numeric(..., errors="coerce")`** turns what it cannot convert into
  `NaN` instead of stopping the program.
- **There are three options for missing values** and none is always right;
  you have to state your decision in the report.
- `dropna(subset=[...])` is usually better than a bare `dropna()`.
- **Duplicates** are found with `duplicated` and
  `drop_duplicates(subset=...)`.
- **Ask why an outlier is there before deleting it.**
- The order matters: names → text → types → duplicates → missing.
- Keep the raw data and work on a copy.
