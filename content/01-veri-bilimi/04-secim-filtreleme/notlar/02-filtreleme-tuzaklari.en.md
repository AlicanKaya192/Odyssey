# Filtering Traps

## 1. After filtering, the index is full of holes

```python
data = pd.DataFrame({"name": ["Ada", "Kerem", "Mina"], "score": [82, 74, 91]})
high = data[data["score"] > 80]
print(high.index.tolist())
```

```text
[0, 2]
```

The number of the row that was not selected is **skipped**. This is
deliberate: you do not lose where each row came from.

But it has two consequences:

- `high.loc[1]` now raises a `KeyError` — that label is not there.
- If you combine with another Series, **alignment** produces `NaN`s you did
  not expect because of the gapped index.

To renumber: `high.reset_index(drop=True)`.

## 2. `iloc[0]` and `loc[0]` mean different things after filtering

```python
high.iloc[0]    # always the first row
high.loc[0]     # the row labelled "0" - KeyError if it is gone
```

If you want the first row, `iloc[0]`. `loc[0]` only works if the label `0`
is still there, and the filter may have removed it.

**The rule:** if you say "first", "last" or "third", use `iloc`; if you are
looking for a name or a code, use `loc`.

## 3. `&` without parentheses

```python
data[data["score"] > 70 & data["score"] < 90]
```

```text
ValueError: The truth value of a Series is ambiguous.
```

The `&` operator runs **before** `>` and `<`, so pandas is handed something
meaningless.

The correct form wraps each condition in parentheses:

```python
data[(data["score"] > 70) & (data["score"] < 90)]
```

You are lucky to get an error here; in some expressions you get a wrong
answer without any error at all.

## 4. `&` instead of `and`

```python
data[(data["a"] > 1) and (data["b"] < 5)]     # ValueError
data[(data["a"] > 1) & (data["b"] < 5)]       # correct
```

`and` expects a single truth value; you have one per row. The same reason as
in NumPy.

**The exception:** inside `query`, `and` **does** work, because that is not
Python:

```python
data.query("a > 1 and b < 5")
```

## 5. An empty result passes silently

```python
selected = data[data["score"] > 1000]
print(selected.shape)
print(selected["score"].mean())
```

```text
(0, 2)
nan
```

No rows were left but there is no error. The average comes out as `nan` and
that is what goes into your report.

You need to check after filtering:

```python
if selected.empty:
    ...
```

`len(selected)` or `selected.shape[0]` does the same job.

## 6. A filtered table is a copy

```python
high = data[data["score"] > 80]
high["score"] = 0
print(data["score"].tolist())
```

```text
[82, 74, 91]
```

The original did not change. In pandas 3.0 the result of a filter is a real
**copy**; modifying it does not touch the source.

That sounds like good news, but it is a trap in the other direction: if you
want to change the original, assigning to a filtered result does nothing.
You need a single `loc` call:

```python
data.loc[data["score"] > 80, "score"] = 0
```

## 7. Chained assignment

```python
data[data["score"] > 80]["score"] = 0     # nothing happens
data.loc[data["score"] > 80, "score"] = 0 # the correct form
```

The same thing as the previous one, but harder to spot because it is on one
line. An intermediate table is produced, the assignment goes into it, and it
is thrown away.

**The rule:** never use square brackets **twice in a row** when modifying.

## 8. `between` includes both ends

```python
pd.Series([1, 2, 3]).between(1, 3)
```

```text
[True, True, True]
```

`between(1, 3)` means "1 and 3 included". If you are used to Python slices
you may read it as `1 <= x < 3`.

To leave an end out you have to say so:

```python
s.between(1, 3, inclusive="left")
```

## 9. `loc` slices include the end

```python
by_name.loc["Ada":"Mina"]     # Mina included
data.iloc[0:3]                # the third row excluded
```

Two different rules for two different tools. If they give the same number of
rows, that is a coincidence.

A `loc` slice also gives unexpected results when the **index is not sorted**
— on an unsorted index, "from a to c" is ambiguous.

## 10. `str` methods and missing values

```python
pd.Series(["Ada", None]).str.contains("A")
```

```text
[True, False]
```

A missing value counts as `False` and drops out of the filter. Usually that
is what you want, but if you want to see the missing ones too you have to
check for them separately:

```python
mask = data["name"].str.contains("A") | data["name"].isna()
```

## 11. Case matches exactly

```python
data[data["city"] == "ankara"]     # comes back empty
data[data["city"] == "Ankara"]     # correct
```

In real data the same city arrives in three different spellings.
Standardising before comparing is a good habit:

```python
data["city"] = data["city"].str.strip().str.title()
```

Or make the comparison case-insensitive:

```python
data[data["city"].str.lower() == "ankara"]
```

## 12. `nlargest` takes the first one on a tie

```python
data.nlargest(2, "score")
```

If two rows have the same score, which one comes back depends on the **order
they were entered**. The result is stable but not "fair".

If you want to break the tie yourself, give a second criterion:

```python
data.sort_values(["score", "age"], ascending=[False, True]).head(2)
```
