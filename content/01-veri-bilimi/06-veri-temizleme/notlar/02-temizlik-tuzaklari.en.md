## 1. `dropna()` drops more rows than you think

```python
d = pd.DataFrame({"a": [1, None, 3], "b": [None, 2, 3]})
print(d.dropna().shape)
print(d.dropna(subset=["a"]).shape)
```

```text
(1, 2)
(2, 2)
```

A bare `dropna()` drops a row if **any** column is empty. One row survived
out of three.

On a table with twenty columns that means losing half your data — because of
columns you do not even care about.

**The right way:** say which column has to be filled.

```python
data.dropna(subset=["score"])
```

## 2. Filling with zero distorts the mean

```python
s = pd.Series([1.0, None, 3.0])
print(s.mean())
print(s.fillna(0).mean())
```

```text
2.0
1.3333333333333333
```

Treating a missing value as zero says "the measurement was zero". The average
drops and the data looks worse than it is.

If zero **really is** the right answer (no sales = 0 sales), fill it. If it
means "unknown", do not fill it, or fill it with the mean.

## 3. Filling with the mean reduces the spread

Does filling with the mean preserve the mean? It does. But it **lowers the
standard deviation**: every value you add sits exactly in the middle and the
data looks more consistent than it is.

With few gaps that is fine; with many, your model or report becomes
misleading.

When there are extreme values, filling with the **median** is safer:

```python
s = pd.Series([1, 2, 3, 100])
print(s.mean())      # 26.5
print(s.median())    # 2.5
```

## 4. `astype(int)` does not work with missing values

```python
pd.Series([1.0, None]).astype(int)
```

```text
IntCastingNaNError
```

The integer type cannot hold `NaN`. You have to deal with the gaps first:

```python
s.fillna(0).astype(int)
s.dropna().astype(int)
```

Also, `astype(int)` **truncates** rather than rounding: `1.9` becomes `1`. If
you want rounding, call `round()` first.

## 5. Without `to_numeric`, one broken cell stops the program

```python
data["score"].astype(float)     # ValueError if "abc" is there
pd.to_numeric(data["score"], errors="coerce")   # "abc" becomes NaN
```

There is always a broken cell in real data. `errors="coerce"` confines the
problem to that one cell.

Afterwards you can see how many broke:

```python
clean = pd.to_numeric(data["score"], errors="coerce")
print(clean.isna().sum() - data["score"].isna().sum())
```

The same argument exists for `pd.to_datetime`.

## 6. Fake missing values

In real data "missing" is often not `NaN`: `-1`, `0`, `999`, `"unknown"`,
`"N/A"`, an empty string.

```python
print(pd.Series([1, -1, 3]).mean())    # 1.0 -- wrong
```

If `-1` means "unknown", it gets mixed into the average and ruins the
result.

**One of the first jobs** is turning these into real `NaN`:

```python
data["score"] = data["score"].replace(-1, np.nan)
data["city"] = data["city"].replace(["", "N/A", "unknown"], np.nan)
```

Do not assume the data is clean because `isna().sum()` is zero; first find
out which values mean "missing".

## 7. Grouping before cleaning the text

```python
data.groupby("city").size()
```

`"Ankara"`, `"ankara"` and `"Ankara "` become **three separate groups**. The
counts are split and none of them is right.

Before grouping:

```python
data["city"] = data["city"].str.strip().str.title()
```

A way to check: if `data["city"].nunique()` is larger than you expect, there
are inconsistent spellings.

## 8. `str` methods do not work without `.str`

```python
data["city"].lower()        # AttributeError
data["city"].str.lower()    # correct
```

`data["city"]` is not a string but a **Series of strings**.

The same structure exists as `.dt` for dates and `.cat` for categories.

## 9. The invisible space in a column name

```python
list(pd.DataFrame({" a ": [1]}).columns)
```

```text
[' a ']
```

On screen it looks like `a`, but the real name is `" a "`. Write `data["a"]`
and you get a `KeyError` whose cause you cannot see.

**The first job:**

```python
data.columns = data.columns.str.strip().str.lower()
```

## 10. Which one does `drop_duplicates` keep?

```python
pd.DataFrame({"a": [1, 1, 2]}).drop_duplicates().index.tolist()
```

```text
[0, 2]
```

By default the **first** record is kept. If you want to keep the updated one
you have to say `keep="last"`.

Which is correct depends on the data: in records arriving in date order, the
last one is usually the current one.

Looking before deleting is a good habit:

```python
data[data.duplicated(keep=False)]   # shows all the duplicates
```

## 11. `duplicated()` looks at every column

```python
data.duplicated()                    # every column has to match
data.duplicated(subset=["id"])       # identity only
```

If the same student was entered twice but one of the scores differs, a bare
`duplicated()` does not count it as a duplicate.

In real data you usually look at an **identity column**: if the same number
appears twice, that is a duplicate even if the other columns differ.

## 12. Deleting an outlier without knowing why it is there

When you find an outlier the question is: **is it a real extreme value or a
data-entry mistake?**

- 1000 in an exam scored out of 100 → a mistake; fix it or drop it.
- 900 thousand in a salary list → could be real; the CEO is an employee too.

Deleting without knowing is **prettifying** the data, not cleaning it. And
you have to say in your report that you deleted it.

`clip` is a middle ground: it pulls the value to the bound without losing the
record.

## 13. Writing the cleaned data over the raw file

```python
data.to_csv("data.csv", index=False)    # the raw data is gone
data.to_csv("clean.csv", index=False)   # the right way
```

You discover a mistake in your cleaning steps days later. If the raw data is
still there you start again; if not, there is nothing to be done.

For the same reason, work on a copy in memory too: `data = raw.copy()`.
