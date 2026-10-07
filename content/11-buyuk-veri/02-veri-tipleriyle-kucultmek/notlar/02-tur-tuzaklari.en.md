Changing types is usually silent: when something goes wrong pandas mostly
raises no error, the result just comes out wrong. Every trap on this page was
tried on this machine.

## 1. `astype` breaks what overflows

```python
pd.Series([100, 200, 300]).astype("int8").tolist()
# [100, -56, 44]
```

No error, no warning. Look at `min()` / `max()` first, or use
`pd.to_numeric(..., downcast="integer")`.

## 2. Arithmetic overflows too

```python
small = pd.Series([100, 120, 127]).astype("int8")
(small + 1).tolist()
# [101, 121, -128]
```

If a column has a small type, what you add to it or multiply it by stays in
the same type. If the sum or product will grow, widen first:
`small.astype("int64") * 1000`.

## 3. A `float32` total drifts

The total of a million prices drifts by 15 lira inside `float32`. Store as
`float32`, add up as `float64`:

```python
total = prices32.astype("float64").sum()
```

## 4. Text with many different values grows as `category`

The `order_time` column, with 984 369 different values, went from 25.8 MB
to 29.3 MB as `category`. Check `nunique()` first.

## 5. A value not in the list cannot be written to a `category` column

```python
c = pd.Series(["card", "cash", "card"], dtype="category")
c[0] = "crypto"
# TypeError: Cannot setitem on a Categorical with a new category (crypto) ...
```

Add the category first: `c = c.cat.add_categories(["crypto"])`.

## 6. Joining two columns with different categories loses the type

```python
a = pd.Series(["x", "y"], dtype="category")
b = pd.Series(["y", "z"], dtype="category")
pd.concat([a, b]).dtype      # str
pd.concat([a, a]).dtype      # category
```

When you read in pieces and join them (Section 3) you may need to make the
result `category` again.

## 7. A missing value turns whole numbers into decimals

```python
pd.Series([1, 2, None, 4]).dtype     # float64
```

For whole numbers with missing values use the capitalised `Int8` …
`Int64`.

## 8. Day first or month first?

```python
pd.to_datetime(pd.Series(["03/04/2024"])).iloc[0].month                 # 3
pd.to_datetime(pd.Series(["03/04/2024"]), dayfirst=True).iloc[0].month   # 4
```

By default pandas reads the month first (the American form). If the day is
written first, as in Turkey, use `dayfirst=True` or, better, an explicit
form: `format="%d/%m/%Y"`.
