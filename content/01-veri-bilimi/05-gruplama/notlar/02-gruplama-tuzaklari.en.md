# Grouping Traps

## 1. Rows with a missing key drop out silently

```python
d = pd.DataFrame({"g": ["a", "a", None], "v": [1, 2, 3]})
print(d.groupby("g")["v"].sum())
```

```text
g
a    3
Name: v, dtype: int64
```

The total should have been 6. The third row's key was empty, so it joined no
group and **vanished from the result entirely**.

No error, no warning. The total in your report is wrong and finding out why
takes hours.

**To see them:**

```python
d.groupby("g", dropna=False)["v"].sum()
```

**A habit worth having:** run `data["g"].isna().sum()` before grouping.

## 2. `count()` and `size()` are not the same

```python
d = pd.DataFrame({"g": ["a", "a", "b"], "v": [1.0, None, 3.0]})
print(d.groupby("g")["v"].count().tolist())
print(d.groupby("g").size().tolist())
```

```text
[1, 1]
[2, 1]
```

`count()` counts the **filled** cells, `size()` counts **all** rows. Group
`a` has two rows but one of them is empty.

If you write `count()` to answer "how many records are in this group", you
miss the rows with missing values.

## 3. Calculations skip the missing ones

```python
print(d.groupby("g")["v"].mean())
```

```text
g
a    1.0
b    3.0
```

Group `a`'s mean is 1.0 because the second value was empty and did not enter
the calculation. This is the same behaviour as on a Series: pandas skips the
missing ones.

Is that right? It depends. But you should not trust an average **without
knowing how many values were skipped**. Look at `count()` and `size()`
together.

## 4. `sum()` of an all-empty group gives zero

```python
d = pd.DataFrame({"g": ["a"], "v": [np.nan]})
print(d.groupby("g")["v"].sum())
```

```text
g
a    0.0
```

There is no data at all, but the total is 0.0. In this situation `mean()`
gives `nan` while `sum()` gives zero.

Zero and "no data" are not the same thing. When you see a zero in a report
you have to be able to tell whether it is a measurement or a gap.

## 5. The group key moves into the index

```python
result = data.groupby("city")["score"].mean()
print(result["Ankara"])       # works
print(result[0])              # does not - KeyError
```

After `groupby` the key is the **index**, not a column. That causes trouble
if you want to join the result with a table.

Two fixes:

```python
data.groupby("city", as_index=False)["score"].mean()   # the key stays a column
data.groupby("city")["score"].mean().reset_index()     # convert afterwards
```

## 6. `[...]` and `[[...]]` matter here too

```python
data.groupby("c")["s"].mean()      # a Series
data.groupby("c")[["s"]].mean()    # a one-column table
```

The same rule as on a DataFrame. Use the second if you are going to join the
result with a table, the first if you are going to call Series methods like
`idxmax()` on it.

## 7. `agg` rather than `apply`

```python
data.groupby("c")["s"].apply(lambda x: x.max() - x.min())   # works
data.groupby("c")["s"].agg(lambda x: x.max() - x.min())     # same result, faster
```

`apply` goes back into Python for every group and builds a group object;
`agg` works more directly.

If a built-in calculation exists (`mean`, `sum`, `max`), passing its name is
fastest: `agg("mean")`. A lambda is only for calculations that have no
built-in.

## 8. Groups come out sorted alphabetically

```python
data.groupby("city")["score"].mean()
```

The result is alphabetical regardless of the order in the data.

Usually that is fine, but it causes trouble in two cases: when the key has a
natural order (month names, "low/medium/high"), alphabetical order is
meaningless.

If you want your own order, sort afterwards:

```python
result.sort_values(ascending=False)
result.reindex(["low", "medium", "high"])
```

You can also pass `sort=False`, which keeps the order of first appearance in
the data.

## 9. `NaN` in a pivot table is not zero

```python
data.pivot_table(index="city", columns="grade", values="score", aggfunc="mean")
```

An empty cell means that combination **does not exist in the data**. Nobody
in Ankara has grade C — that does not mean "the C average in Ankara is
zero".

You can fill them with `fill_value=0`, but be aware of what you are saying:
in later calculations those zeros behave like real measurements and drag the
averages down.

## 10. `transform` and `agg` get confused

```python
data.groupby("city")["score"].mean()             # 3 rows (one per group)
data.groupby("city")["score"].transform("mean")  # 6 rows (one per row)
```

Both compute the group mean, but the results are different sizes.

- Producing a report: `agg` / `mean`.
- Comparing each row with its own group: `transform`.

You can add a `transform` result to the table as a column directly; you
cannot do that with an `agg` result, the lengths do not match.

## 11. A MultiIndex is awkward to work with

```python
result = data.groupby(["city", "grade"])["score"].mean()
print(result["Ankara"])          # works
print(result["Ankara", "A"])     # works
print(result.loc["A"])           # does not
```

Grouping by two keys gives a two-level index and the selection rules change.

Most of the time flattening is easier:

```python
result.reset_index()     # an ordinary table
result.unstack()         # the second key becomes columns (like a pivot)
```

## 12. Finding the "best row" per group

The wrong attempt:

```python
data.groupby("city")["score"].max()      # only numbers, no idea whose
```

The correct way, in two steps:

```python
data.loc[data.groupby("city")["score"].idxmax()]
```

`idxmax()` gives one **row label** per group and `loc` fetches those whole
rows — with the name, the city and the score.

**Careful:** on a tie within a group, `idxmax` takes the first row.
