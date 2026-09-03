pandas makes things convenient by quietly making decisions for you. These are
the places where those decisions surprise you.

## 1. `s[0]` looks for a label, not a position

```python
s = pd.Series([10, 20, 30], index=[2, 0, 1])
print(s[0])
```

```text
20
```

You expected the first element and got the element carrying the **label**
`0`.

When the index is made of numbers, square brackets become ambiguous. That is
why pandas gives you two explicit ways:

```python
print(s.loc[0])    # by label    -> 20
print(s.iloc[0])   # by position -> 10
```

**The rule:** if you want a position, always write `iloc`. Then you never
have to think about what the index happens to be.

## 2. If you do not assign the result, it is lost

```python
values = pd.Series([1.0, None, 3.0])
values.fillna(0)
print(values.isna().sum())
```

```text
1
```

`fillna` returned a new Series, you did not put it anywhere, and it
disappeared. The original never changed.

```python
values = values.fillna(0)
```

Almost **every method** in pandas is like this: `dropna`, `sort_values`,
`astype`, `round`, `replace`. All of them return a new object.

## 3. Alignment can give you an answer you did not expect

Alignment usually saves you, but sometimes it surprises you:

```python
a = pd.Series([1, 2, 3])
b = pd.Series([1, 2, 3], index=[2, 1, 0])

print((a + b).tolist())
```

```text
[4, 4, 4]
```

You expected `[2, 4, 6]`. pandas matched on labels, not order: 0 with 0
(1+3), 1 with 1 (2+2), 2 with 2 (3+1).

**When does this happen:** when you filter a Series and then combine it with
another one. Filtering keeps the index, so the numbers in between are
missing.

**The fix:** if you do not want alignment, reset the index or work with the
values:

```python
print((a.values + b.values).tolist())            # [2, 4, 6]
print((a + b.reset_index(drop=True)).tolist())   # [2, 4, 6]
```

## 4. Missing values are skipped silently

```python
scores = pd.Series([80.0, None, None, None, 90.0])
print(scores.mean())
print(scores.count())
```

```text
85.0
2
```

An average came back and it looks reasonable. But **three of the five**
records were empty and that average was computed from two numbers.

NumPy would have given `nan` and warned you. pandas does not warn — it gives
you the convenience and leaves the responsibility with you.

**Make it a habit:** compare `count()` with `size` before you take an
average.

If you want the missing ones to count, you say so:

```python
print(scores.sum(skipna=False))   # nan
```

## 5. The mean of an empty Series is `nan`

```python
empty = pd.Series([], dtype=float)
print(empty.mean())
```

```text
nan
```

In plain Python `sum([]) / len([])` raised a division-by-zero error; pandas
does not raise, it gives `nan`.

This comes up often after filtering: if no rows are left the average becomes
`nan`, and if you do not notice you write `nan` into your report.

## 6. Adding `None` turns the type into decimal

```python
print(pd.Series([1, 2, 3]).dtype)
print(pd.Series([1, None, 3]).dtype)
```

```text
int64
float64
```

The integer type cannot hold `NaN`, so pandas converts the Series to
decimal. The result: you see `1.0` where you expected `1`.

Converting back does not work while a missing value is there:

```python
pd.Series([1.0, None, 3.0]).astype(int)
```

```text
IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer.
```

You have to deal with the gaps first: `dropna()` or `fillna(...)`, then
`astype(int)`.

## 7. `Series.unique()` does not sort

```python
cities = pd.Series(["Izmir", "Ankara", "Izmir", "Bursa"])
print(list(cities.unique()))
```

```text
['Izmir', 'Ankara', 'Bursa']
```

`np.unique` sorted alphabetically; `Series.unique()` keeps the **order of
first appearance**. Two functions with the same name, two different
behaviours.

If you want them sorted you write `sorted(cities.unique())`.

## 8. Text methods do not work without `.str`

```python
cities.lower()
```

```text
AttributeError: 'Series' object has no attribute 'lower'
```

`cities` is not a string but a **Series of strings**. The methods come
through `.str`:

```python
print(cities.str.lower().tolist())
```

The same thing happens with `.dt` for dates and `.cat` for categories.

## 9. `apply` works but is slow

```python
values.apply(lambda x: x * 2)   # works
values * 2                       # same result, much faster
```

`apply` calls a Python function for every element; it gives back all the
speed a vectorised operation earned you.

**The rule:** if there is a vectorised equivalent, use it. `apply` is for
work that is genuinely complex and has to be thought about row by row.

## 10. `value_counts` does not count the missing ones

```python
s = pd.Series(["a", "b", None, "a"])
print(s.value_counts().sum())
print(s.size)
```

```text
3
4
```

By default `NaN` is not counted. If you want it counted you say so:

```python
print(s.value_counts(dropna=False))
```

If you write `value_counts().sum()` to answer "how many records are there in
this categorical column", you miss the empty ones.
