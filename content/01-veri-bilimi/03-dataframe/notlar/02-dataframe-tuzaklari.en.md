# DataFrame Traps

## 1. Chained assignment does nothing

```python
data[data["a"] > 1]["b"] = 99
print(data["b"].tolist())
```

```text
[4, 5, 6]
```

Nothing changed. `data[data["a"] > 1]` produced a **new table**, the
assignment went into that, and it was thrown away immediately.

pandas notices and raises a `ChainedAssignmentError` warning — but the
program does not crash, what you wanted simply does not happen.

**The correct form, in one step with `loc`:**

```python
data.loc[data["a"] > 1, "b"] = 99
print(data["b"].tolist())
```

```text
[4, 99, 99]
```

**The rule:** if you are going to modify a table, never use square brackets
**twice in a row**. Selection and assignment belong in a single `loc` call.

## 2. Assignment does not make a copy

```python
first = pd.DataFrame({"a": [1, 2]})
second = first
second["a"] = [9, 9]
print(first["a"].tolist())
```

```text
[9, 9]
```

`second = first` does not build a new table, it gives **a second name to the
same table**. Change one and the other changes.

If you want a real copy: `second = first.copy()`.

This is the DataFrame version of NumPy's slice-is-a-view problem. The same
risk exists when you pass a table into a function: if the function modifies
it, the caller's table changes too.

## 3. `data["x"]` and `data[["x"]]` are not the same

```python
type(data["score"])     # Series
type(data[["score"]])   # DataFrame
```

Single square brackets give a **Series**, double square brackets a
**one-column table**.

Why it matters: their methods differ. A Series has `str.lower()`, a table
does not. On a table `shape` gives two values, on a Series one.

Where it hurts: when a function expects a Series and you hand it a table, or
the other way round. The error is usually an `AttributeError` and it takes a
while to work out why.

## 4. `describe()` skips text columns

```python
data.describe()
```

Only the numeric columns appear. At first glance it looks like half your
columns vanished, but nothing is lost — a text column has no average, so it
is left out.

If you want to see the text columns too:

```python
data.describe(include="all")
```

For the same reason `data.mean()` does not work directly:

```text
TypeError: Cannot perform reduction 'mean' with string dtype
```

You have to say `data.mean(numeric_only=True)`.

## 5. `len(data)` is rows, `data.size` is cells

```python
len(data)      # 3   rows
data.size      # 6   cells (3 x 2)
data.shape     # (3, 2)
```

`size` is a name inherited from NumPy and means **total cells**. For the
number of rows use `len(data)` or `data.shape[0]`.

On a Series `size` was the number of rows; on a table its meaning changes.
The same name behaving differently on two structures is confusing.

## 6. The mean of an empty table is `nan`

```python
empty = data[data["score"] > 1000]
print(empty.shape)
print(empty["score"].mean())
```

```text
(0, 3)
nan
```

If a filter leaves no rows, calculations give `nan` rather than an error. To
avoid writing `nan` into a report, check `shape[0]` or `empty` after
filtering.

## 7. Spaces in column names

```python
list(pd.DataFrame({" a ": [1]}).columns)
```

```text
[' a ']
```

Leading and trailing spaces in column names coming from a CSV are **kept**.
Write `data["a"]` and you get a `KeyError` whose cause is invisible on
screen.

Cleaning them first is a good habit:

```python
data.columns = data.columns.str.strip()
```

Case matches exactly too: `"Score"` and `"score"` are different columns.

## 8. `append` is gone

```python
data.append(other)
```

```text
AttributeError: 'DataFrame' object has no attribute 'append'
```

It appears in a lot of older tutorials, but it was **removed in pandas
2.0**. Use this instead:

```python
pd.concat([data, other])
```

Adding rows in a loop was a bad idea anyway: every call rebuilt the table
from scratch. The right way is to collect the rows in a list and build the
table once at the end.

## 9. Going row by row is a last resort

```python
for index, row in data.iterrows():
    ...
```

It works, but it creates a **Series** object for every row and is very slow.
If there is a vectorised equivalent, use it:

```python
data["total"] = data["price"] * data["count"]   # correct
```

`iterrows` is only for work where the rows genuinely depend on each other
(deciding based on the previous one, for instance).

## 10. Column order is the order in the dictionary

```python
list(pd.DataFrame({"z": [1], "a": [2]}).columns)
```

```text
['z', 'a']
```

pandas does not sort the columns alphabetically; they stay in the order you
wrote them. If you want a particular order you select it explicitly:

```python
data = data[["name", "city", "score"]]
```

This is one of the last things to do before saving a table or putting it in
a report.
