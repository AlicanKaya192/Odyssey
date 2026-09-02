# Grouping and Aggregation

In the first section you wrote ten lines to compute the average score per
city: two dictionaries, a loop and a division. Now you will learn the
one-line equivalent of those ten lines.

```python
data.groupby("city")["score"].mean()
```

This section is about that line and what surrounds it.

The examples use this table:

```python
data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "grade": ["A", "B", "A", "C", "B", "A"],
    "score": [82, 74, 91, 68, 88, 76],
})
```

## Split, apply, combine

`groupby` is a three-step operation:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Split</b><br>divide the rows into buckets by a key</span>
    <span class="arrow">→</span>
    <span class="node"><b>Apply</b><br>produce one number per bucket</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Combine</b><br>gather the results into one table</span>
  </div>
  <figcaption>You only say "by what" and "what to compute"; pandas does all three steps.</figcaption>
</figure>

```python
print(data.groupby("city")["score"].mean())
```

```text
city
Ankara    87.0
Bursa     68.0
Izmir     75.0
Name: score, dtype: float64
```

The result is a **Series**: the groups are the index and the values are the
computed numbers. The groups come out **sorted alphabetically** by
themselves.

Read it left to right: *"group `data` by `city`, take the `score` column,
compute its mean."*

## Which calculation?

Whatever a Series has is available here:

```python
print(data.groupby("city")["score"].count())
print(data.groupby("city").size())
```

```text
city
Ankara    3
Bursa     1
Izmir     2
Name: score, dtype: int64
city
Ankara    3
Bursa     1
Izmir     2
dtype: int64
```

They look alike but differ: **`count()` counts filled cells** and **`size()`
counts all rows**. With missing values the two diverge.

`sum`, `min`, `max`, `median`, `std` and `nunique` all work the same way.

## Several calculations: agg

```python
print(data.groupby("city")["score"].agg(["count", "mean", "max"]))
```

```text
        count  mean  max
city
Ankara      3  87.0   91
Bursa       1  68.0   68
Izmir       2  75.0   76
```

The result is now a **table**: groups as rows, calculations as columns.

You can also name the columns yourself and compute from different columns:

```python
print(data.groupby("city").agg(
    people=("name", "count"),
    average=("score", "mean"),
))
```

```text
        people  average
city
Ankara       3     87.0
Bursa        1     68.0
Izmir        2     75.0
```

The form is `new_name=("which column", "which calculation")`. This is the
shape you will use most when producing a report.

## Grouping by two keys

```python
print(data.groupby(["city", "grade"])["score"].mean())
```

```text
city    grade
Ankara  A        86.5
        B        88.0
Bursa   C        68.0
Izmir   A        76.0
        B        74.0
Name: score, dtype: float64
```

The index has two levels — this is called a **MultiIndex**. The cells that
look empty mean "the same as the one above"; they are simply not repeated.

Working with that structure is a little awkward, so it is usually flattened:

```python
print(data.groupby(["city", "grade"])["score"].mean().reset_index())
```

`reset_index()` turns the levels into columns and leaves you with an ordinary
table.

## The group key becomes the index

After `groupby` the key moves into the **index**. If you want it to stay a
column:

```python
print(data.groupby("city", as_index=False)["score"].mean())
```

```text
     city  score
0  Ankara   87.0
1   Bursa   68.0
2   Izmir   75.0
```

This shape is more useful if you are going to join the result with another
table or write it to a file.

## Pivot table

The **table form** of grouping by two keys:

```python
print(data.pivot_table(index="city", columns="grade", values="score", aggfunc="mean"))
```

```text
grade      A     B     C
city
Ankara  86.5  88.0   NaN
Bursa    NaN   NaN  68.0
Izmir   76.0  74.0   NaN
```

One key as rows, the other as columns, the calculation in the cells. The same
thing as a pivot table in Excel.

The `NaN` cells mean "this combination does not exist in the data" — nobody
in Ankara has grade C. Not zero, but **absent**. The two should not be
confused; but if you want to see zeros you can say so:

```python
data.pivot_table(..., fill_value=0)
```

## Sorting and finding the top

A group result is also a Series, so you can do anything to it:

```python
averages = data.groupby("city")["score"].mean()

print(averages.sort_values(ascending=False))
print(averages.idxmax())
```

```text
city
Ankara    87.0
Izmir     75.0
Bursa     68.0
Name: score, dtype: float64
Ankara
```

`idxmax()` gives the **name of the group** with the highest average. These
two lines are exactly the answer to "which city has the highest sales".

## transform: spreading the group result across the rows

Sometimes you want the group average **next to every row** — for a question
like "is this student above their own city's average?":

```python
data["city_mean"] = data.groupby("city")["score"].transform("mean")
print(data[["name", "city", "score", "city_mean"]])
```

```text
    name    city  score  city_mean
0    Ada  Ankara     82       87.0
1  Kerem   Izmir     74       75.0
2   Mina  Ankara     91       87.0
3  Deniz   Bursa     68       68.0
4    Efe  Ankara     88       87.0
5   Sila   Izmir     76       75.0
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>agg / mean</h4>
      <p>Returns <b>one row per group</b>. The table shrinks.</p>
    </div>
    <div class="versus-side">
      <h4>transform</h4>
      <p>Writes each group's result onto every row. The table stays the <b>same size</b>.</p>
    </div>
  </div>
</figure>

Now you can compare:

```python
data["above_city"] = data["score"] > data["city_mean"]
```

## Rows with a missing key drop out silently

```python
d = pd.DataFrame({"g": ["a", "a", None], "v": [1, 2, 3]})
print(d.groupby("g")["v"].sum())
```

```text
g
a    3
Name: v, dtype: int64
```

The third row's key is empty, so it **joined no group** and vanished from the
result entirely. The total should be 6 but shows as 3.

This is a good example of a silent bug. If you want to see them:

```python
print(d.groupby("g", dropna=False)["v"].sum())
```

```text
g
a      3
NaN    3
Name: v, dtype: int64
```

**A habit worth having:** run `isna().sum()` on the key column before
grouping.

## Summary

- `groupby` is three steps: **split, apply, combine.**
- The result is a Series; the key moves into the **index** and the groups
  come out sorted alphabetically.
- `count()` counts filled cells and `size()` counts all rows.
- **`agg`** does several calculations at once;
  `new_name=("column", "calculation")` is the reporting form.
- `as_index=False` leaves the key as a column.
- **`pivot_table`** is the table form of grouping by two keys; empty cells
  are `NaN`.
- **`transform`** spreads the group result across the rows and keeps the
  table the same size.
- **Rows with a missing key drop out silently.** `dropna=False` makes them
  visible.
