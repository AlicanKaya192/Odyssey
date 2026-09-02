# DataFrame Basics

A Series was a single column: scores, prices, cities. Real data has **more
than one column**: who, where, how many, when.

A **DataFrame** is a table made of Series placed side by side. It is the
structure you will work with for the rest of this path.

```python
import pandas as pd
```

## Your first table

The most common way is to build one from a dictionary — the **keys become
column names** and the values the contents of the columns:

```python
data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa"],
    "score": [82, 74, 91, 68],
})

print(data)
```

```text
    name    city  score
0    Ada  Ankara     82
1  Kerem   Izmir     74
2   Mina  Ankara     91
3  Deniz   Bursa     68
```

The index is on the left and the column names across the top. The list of
dictionaries from the first section was exactly this; now you no longer have
to work through it with a loop.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">row</span><span class="anat-body">one record; the index names it</span></div>
    <div class="anat-row"><span class="anat-label">column</span><span class="anat-body">one attribute; each column is really a <b>Series</b></span></div>
    <div class="anat-row"><span class="anat-label">index</span><span class="anat-body">the row labels — every column shares them</span></div>
    <div class="anat-row"><span class="anat-label">columns</span><span class="anat-body">the column labels; itself an index</span></div>
  </div>
</figure>

It can also be built from a list of dictionaries — data from a CSV or an API
usually arrives in that shape:

```python
rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
print(pd.DataFrame(rows))
```

```text
   a  b
0  1  2
1  3  4
```

## A first look at a table

There are four questions you ask when you first open a dataset, and each has
a one-line answer:

```python
print(data.shape)
print(list(data.columns))
print(data.dtypes)
print(data.head(2))
```

```text
(4, 3)
['name', 'city', 'score']
name       str
city       str
score    int64
dtype: object
    name    city  score
0    Ada  Ankara     82
1  Kerem   Izmir     74
```

- `shape` → **(rows, columns)**. How many records, how many attributes.
- `columns` → the column names. The fastest way to spot a typo.
- `dtypes` → the type of each column. If a column that should be numeric
  shows up as `str`, something is wrong there.
- `head()` → the first rows. Do not talk about data you have not looked at.

In the `dtypes` output the text columns say `str`. Older documentation shows
`object` instead; this changed in pandas 3.0.

## Selecting columns

Ask for one column and you get a **Series** back:

```python
print(data["score"])
```

```text
0    82
1    74
2    91
3    68
Name: score, dtype: int64
```

The Series' `name` attribute carries the column name — that was the link
mentioned in the previous section.

Ask for several and you get a **DataFrame** back. Note the **nested square
brackets**.

```python
print(data[["name", "score"]])
```

```text
    name  score
0    Ada     82
1  Kerem     74
2   Mina     91
3  Deniz     68
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>data["score"]</h4>
      <p>One column → a <b>Series</b>. Series methods like <code>mean()</code> and <code>value_counts()</code> work on it.</p>
    </div>
    <div class="versus-side">
      <h4>data[["score"]]</h4>
      <p>A list was given → a <b>DataFrame</b>. A table with one column; still a table.</p>
    </div>
  </div>
  <figcaption>The difference is a single square bracket. You need to know which one you got, because their methods differ.</figcaption>
</figure>

## Adding a column

A new column is computed from the existing ones:

```python
data["bonus"] = data["score"] + 5
data["passed"] = data["score"] >= 75

print(data[["name", "score", "bonus", "passed"]])
```

```text
    name  score  bonus  passed
0    Ada     82     87    True
1  Kerem     74     79   False
2   Mina     91     96    True
3  Deniz     68     73   False
```

No loop. Because a column is a Series, vectorised operations apply as they
are; a comparison produces a column of `True`/`False`.

Removing a column:

```python
print(list(data.drop(columns=["bonus"]).columns))
```

```text
['name', 'city', 'score', 'passed']
```

`drop` returns a **new table**; the original `data` does not change. The
general pandas rule applies here too.

## Sorting

```python
print(data.sort_values("score", ascending=False)[["name", "score"]])
```

```text
    name  score
2   Mina     91
0    Ada     82
1  Kerem     74
3  Deniz     68
```

Look at the index: `2, 0, 1, 3`. The rows moved, but **their labels moved
with them** — you do not lose where each row came from.

## Changing the index

The default index is numbers, but you can make a column the index:

```python
by_name = data.set_index("name")
print(by_name.loc["Mina", "score"])
```

```text
91
```

Now you call a row by its name: `loc[row, column]`.

To undo it, `reset_index()`. Choosing an index is the main subject of the
next section; for now what matters is that the index is **the name of the
rows**.

## A numeric summary

```python
print(data.describe())
```

```text
           score
count   4.000000
mean   78.750000
std     9.979145
min    68.000000
25%    72.500000
50%    78.000000
75%    84.250000
max    91.000000
```

`describe()` takes **only the numeric columns**; `name` and `city` are not in
the output. This is deliberate: there is no such thing as the average of a
text column.

For the same reason you have to say so in aggregation calls:

```python
print(data.mean(numeric_only=True))
```

```text
score    78.75
dtype: float64
```

Without `numeric_only=True` the text columns give you an error.

## Series and DataFrame

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Series</span><span class="anat-body">one column plus an index. <code>mean()</code>, <code>value_counts()</code>, <code>str</code></span></div>
    <div class="anat-row"><span class="anat-label">DataFrame</span><span class="anat-body">many columns plus a shared index. <code>shape</code>, <code>columns</code>, <code>describe()</code></span></div>
  </div>
</figure>

When you pull a column out of a DataFrame you get a Series, and everything
you learned about Series applies. A DataFrame is not a new world; it is where
Series stand together.

## Summary

- A **DataFrame** is Series side by side with a shared index.
- Build it from a dictionary: the **keys become column names**.
- The first four looks: `shape`, `columns`, `dtypes`, `head()`.
- `data["x"]` is a **Series**, `data[["x"]]` is a **DataFrame**. The
  difference is one square bracket.
- A new column is added by assignment:
  `data["bonus"] = data["score"] + 5`.
- `drop`, `sort_values` and `set_index` all return a **new table**.
- `describe()` looks only at numeric columns, and aggregations need
  `numeric_only=True`.
- Text columns are of type `str` in pandas 3.0; this replaced the `object`
  you see in older documentation.
