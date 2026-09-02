# Selecting and Filtering

You have a table and you want **a piece of it**: certain rows, certain
columns, or the ones matching a condition. This is the thing data work does
most often.

pandas has three ways and you need to tell them apart: **`iloc`**
(position), **`loc`** (label) and **conditions**.

The examples in this section use this table:

```python
data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})
```

## iloc: by position

`iloc` uses **position** — just like a list, starting from zero.

```python
print(data.iloc[0, 2])
print(data.iloc[1:3])
```

```text
82
    name    city  score  age
1  Kerem   Izmir     74   23
2   Mina  Ankara     91   22
```

`iloc[row, column]` — rows to the left of the comma, columns to the right.
When slicing, the **end is excluded**, the Python rule: `1:3` gives two rows.

You can pick columns by position too:

```python
print(data.iloc[:, [0, 2]].head(2))
```

```text
    name  score
0    Ada     82
1  Kerem     74
```

The `:` means "all rows".

## loc: by label

`loc` uses **labels**. When the index is numeric it looks like a row number,
but it is really working with labels. To see the difference, let us make the
names the index:

```python
by_name = data.set_index("name")

print(by_name.loc["Mina", "score"])
print(by_name.loc["Ada":"Mina"])
```

```text
91
         city  score  age
name                     
Ada    Ankara     82   21
Kerem   Izmir     74   23
Mina   Ankara     91   22
```

**Careful: in `loc` slices the end is included.** `"Ada":"Mina"` gives three
rows, Mina among them.

This is where it departs from Python and it surprises people. The reason is
sensible: with labels, "the one before Mina" is meaningless — labels need not
have a numeric order.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>iloc[1:3]</h4>
      <p>Position. <b>End excluded</b> — two rows. Like a Python slice.</p>
    </div>
    <div class="versus-side">
      <h4>loc["a":"c"]</h4>
      <p>Label. <b>End included</b> — three rows. "The one before" is not defined for labels.</p>
    </div>
  </div>
</figure>

## Filtering by condition

This is the way you will use most. A comparison produces a `True`/`False`
column; put it inside the square brackets and the rows are filtered:

```python
print(data[data["score"] >= 80])
```

```text
   name    city  score  age
0   Ada  Ankara     82   21
2  Mina  Ankara     91   22
4   Efe  Ankara     88   21
```

Look at the index: `0, 2, 4`. The numbers of the rows that were not selected
are **skipped**, not renumbered. A gapped index after filtering is normal.

## More than one condition

`&` (and), `|` (or), `~` (not). **Each condition in parentheses.**

```python
print(data[(data["score"] >= 80) & (data["city"] == "Ankara")])
```

```text
   name    city  score  age
0   Ada  Ankara     82   21
2  Mina  Ankara     91   22
4   Efe  Ankara     88   21
```

`and` / `or` **do not work** — the same reason as in NumPy: you do not have
one truth value but as many as there are rows.

Forgetting the parentheses is sneakier: `&` runs before the comparison and
computes something completely different without any error.

## Three shortcuts

Three methods that shorten long conditions:

```python
print(data[data["city"].isin(["Izmir", "Bursa"])][["name", "city"]])
print(data[data["age"].between(21, 22)][["name", "age"]])
print(data[data["name"].str.contains("a")][["name"]])
```

```text
    name   city
1  Kerem  Izmir
3  Deniz  Bursa
5   Sila  Izmir
   name  age
0   Ada   21
2  Mina   22
4   Efe   21
   name
0   Ada
2  Mina
5  Sila
```

- `isin` — the short way of chaining many values with `|`.
- `between` — both ends **included**.
- `str.contains` — searching in text; does not work without `.str`.

For the opposite, put `~` in front:

```python
print(data[~data["city"].isin(["Ankara"])][["name", "city"]])
```

```text
    name   city
1  Kerem  Izmir
3  Deniz  Bursa
5   Sila  Izmir
```

## query: writing the condition as text

For when long conditions become unreadable:

```python
print(data.query("score > 80 and city == 'Ankara'"))
```

```text
   name    city  score  age
0   Ada  Ankara     82   21
2  Mina  Ankara     91   22
4   Efe  Ankara     88   21
```

Inside `query`, `and` / `or` **do work**, because that is not Python but
pandas's own small language. Column names go without quotes.

Where it helps: expressions with three or four conditions. With few
conditions the ordinary form is clearer.

## The largest ones

```python
print(data.nlargest(2, "score")[["name", "score"]])
```

```text
   name  score
2  Mina     91
4   Efe     88
```

The same result as `sort_values(...).head(2)`, but in one call and faster on
large data: instead of sorting everything it just finds the top two.

## Changing values by filter

**This needs care.** Selecting and then assigning does not work:

```python
data[data["score"] < 75]["score"] = 0     # NOTHING HAPPENS
```

The correct form is one step with `loc` — the row condition on the left, the
column on the right:

```python
data.loc[data["score"] < 75, "score"] = 0
print(data[["name", "score"]])
```

```text
    name  score
0    Ada     82
1  Kerem      0
2   Mina     91
3  Deniz      0
4    Efe     88
5   Sila     76
```

**The rule:** never use square brackets twice in a row when modifying a
table. Selection and assignment belong in a single `loc` call.

## Which one when?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">iloc</span><span class="anat-body">"the first row", "the last three" — when position genuinely matters</span></div>
    <div class="anat-row"><span class="anat-label">loc</span><span class="anat-body">when labels mean something (a name, a date, a product code) and <b>when assigning</b></span></div>
    <div class="anat-row"><span class="anat-label">condition</span><span class="anat-body">"everyone scoring above 80" — the one used most</span></div>
  </div>
</figure>

In practice you use conditions 80% of the time, `loc` 15% and `iloc` 5%.

## Summary

- **`iloc`** goes by position, **end excluded**.
- **`loc`** goes by label, **end included**. This departs from the Python
  rule.
- Filtering by condition is the most common way; it leaves a **gapped
  index**.
- Combine conditions with `&`, `|` and `~`, and **do not forget the
  parentheses**. `and` does not work.
- `isin`, `between` and `str.contains` shorten long conditions.
- Inside `query`, `and`/`or` work; it reads well with many conditions.
- **Always use a single `loc` call when changing values.** Chained
  assignment silently does nothing.
