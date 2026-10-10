# Combining with pandas

Real data does not come in one table: orders in one file, customers in
another, each month's sales in a separate table. There are three ways to
combine them: matching on a key column (`merge`), stacking below or beside
(`concat`) and matching on the index (`join`). Combining is where pandas
produces the most silent mistakes: rows vanish or multiply, totals shift and
no error message comes. This section covers both the ways and how to catch
these mistakes.

## merge and the four kinds of join

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "customer": [10, 20, 10, 40],
                       "amount": [250, 90, 40, 70]})
customers = pd.DataFrame({"customer": [10, 20, 30], "name": ["Ada", "Can", "Eda"]})
for how in ["inner", "left", "right", "outer"]:
    joined = orders.merge(customers, on="customer", how=how)
    print(how, len(joined), joined["order"].tolist())
print(orders.merge(customers, on="customer", how="left"))
```

```text
inner 3 [1, 2, 3]
left 4 [1, 2, 3, 4]
right 4 [1.0, 3.0, 2.0, nan]
outer 5 [1.0, 3.0, 2.0, nan, 4.0]
   order  customer  amount name
0      1        10     250  Ada
1      2        20      90  Can
2      3        10      40  Ada
3      4        40      70  NaN
```

`on="customer"` is the **key** column with the same name in both tables.
Customer 40 has no record, customer 30 has no order; `how` chooses what
happens to these unmatched ones:

| `how` | Rows kept | Here |
|---|---|---|
| `inner` (default) | only keys on both sides | order 4 **vanished** |
| `left` | all of the left | order 4 is there, its name `NaN` |
| `right` | all of the right | Eda is there, her order `NaN` |
| `outer` | all of both | 5 rows |

- The default is `inner`: an unmatched order drops **silently**. When adding
  information to orders, `how="left"` is almost always what you want; the
  row count should not change.
- A value missing on one side becomes `NaN`; that is why the `order` column
  turned decimal with `right` and `outer`.

## indicator: find what vanished

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "customer": [10, 20, 10, 40],
                       "amount": [250, 90, 40, 70]})
customers = pd.DataFrame({"customer": [10, 20, 30], "name": ["Ada", "Can", "Eda"]})
check = orders.merge(customers, on="customer", how="outer", indicator=True)
print(check["_merge"].value_counts().to_dict())
lost = check.loc[check["_merge"] == "left_only", "order"].astype(int).tolist()
print(lost)
```

```text
{'both': 3, 'left_only': 1, 'right_only': 1}
[4]
```

- `indicator=True` adds a `_merge` column to each row: `both`, `left_only`
  (only on the left), `right_only` (only on the right).
- Looking with `outer` + `indicator` before a merge shows **by name** which
  records do not match: here order 4's customer is not in the customer
  table. It is the first question to ask when cleaning data.

## Row explosion and validate

```python
import pandas as pd

orders = pd.DataFrame({"customer": [10, 10, 20], "amount": [250, 40, 90]})
cities = pd.DataFrame({"customer": [10, 10, 20],
                       "city": ["Izmir", "Ankara", "Bursa"]})
joined = orders.merge(cities, on="customer")
print(len(orders), len(joined))
print(int(joined["amount"].sum()), int(orders["amount"].sum()))
try:
    orders.merge(cities, on="customer", validate="many_to_one")
except pd.errors.MergeError as error:
    print("MergeError:", str(error).splitlines()[0])
```

```text
3 5
670 380
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

- Customer 10 appears **twice** in the right table (two cities). merge makes
  a row for every matching pair: customer 10's 2 orders × 2 cities = 4 rows.
  The 3-row table became 5.
- The result: a revenue total of **670** instead of 380. No error, a wrong
  report.
- `validate` states the kind of merge in advance and stops if it does not
  hold: `"one_to_one"`, `"one_to_many"`, `"many_to_one"`, `"many_to_many"`.
  Adding customer information to orders is `many_to_one`: many orders,
  **one** customer per order.
- A short check: `len(joined) == len(orders)` should hold.

## The key's type and different names

```python
import pandas as pd

sales = pd.DataFrame({"product_id": [1, 2], "qty": [3, 5]})
products = pd.DataFrame({"id": ["1", "2"], "title": ["pen", "cup"]})
try:
    sales.merge(products, left_on="product_id", right_on="id")
except ValueError as error:
    print("ValueError:", str(error).split(".")[0])
products["id"] = products["id"].astype(int)
joined = sales.merge(products, left_on="product_id", right_on="id")
print(joined.columns.tolist())
```

```text
ValueError: You are trying to merge on int64 and str columns for key 'product_id'
['product_id', 'qty', 'id', 'title']
```

- If the key has different names in the two tables, use `left_on` /
  `right_on`. Both columns stay in the result; drop the unneeded one with
  `drop(columns="id")`.
- `1` is a number in one table and `"1"` text in the other: pandas does not
  match them and raises an error. Very common with codes read from CSV (one
  was read as text because of leading zeros). Make the types equal first:
  `astype(int)` or `astype(str)`.

## Columns with the same name: suffixes

```python
import pandas as pd

jan = pd.DataFrame({"city": ["Izmir", "Ankara"], "sales": [80, 120]})
feb = pd.DataFrame({"city": ["Ankara", "Izmir"], "sales": [110, 95]})
both = jan.merge(feb, on="city")
print(both.columns.tolist())
both = jan.merge(feb, on="city", suffixes=("_jan", "_feb"))
print(both)
```

```text
['city', 'sales_x', 'sales_y']
     city  sales_jan  sales_feb
0   Izmir         80         95
1  Ankara        120        110
```

- Columns other than the key that share a name are told apart with `_x` and
  `_y`. Which is which is forgotten two lines later.
- `suffixes=("_jan", "_feb")` gives meaningful names. Even though the orders
  differ, city matched city; merge looks at the key, not the order.

## concat: stacking

```python
import pandas as pd

jan = pd.DataFrame({"city": ["Izmir", "Ankara"], "sales": [80, 120]})
feb = pd.DataFrame({"city": ["Bursa"], "sales": [50], "returns": [2]})
stacked = pd.concat([jan, feb])
print(stacked.index.tolist(), stacked.columns.tolist())
print(pd.concat([jan, feb], ignore_index=True).index.tolist())
months = pd.concat([jan, feb], keys=["jan", "feb"])
print(months.loc["feb", "city"].tolist(), months["returns"].isna().sum())
```

```text
[0, 1, 0] ['city', 'sales', 'returns']
[0, 1, 2]
['Bursa'] 2
```

- `concat` does not match, it **appends**. The way to gather same-shaped
  pieces (each month's file) into one table.
- The indexes stay as they are: `[0, 1, 0]`, that is, a **repeated** label
  (the previous section's trap). `ignore_index=True` numbers from 0 again.
- `keys=` adds an outer level to each piece: the result has a MultiIndex and
  it is clear which row came from which month.
- The columns are united; a column missing from one piece (`returns`) is
  `NaN` in the other's rows: 2 missing.
- Instead of appending one by one in a loop, collect the pieces in a list and
  call `concat` **once**; every append copies the whole table again.

## join: on the index

```python
import pandas as pd

price = pd.DataFrame({"price": [10.0, 4.5]}, index=["pen", "cup"])
stock = pd.DataFrame({"stock": [3, 8, 1]}, index=["cup", "pen", "box"])
print(price.join(stock))
print(stock.join(price, how="inner").index.tolist())
```

```text
     price  stock
pen   10.0      8
cup    4.5      3
['cup', 'pen']
```

- `join` matches two tables **by their indexes**; a shortcut for merge when
  the key is already in the index. Its default is `how="left"`.
- `price.join(stock)`: pen matched stock 8, cup 3; box has no price, so it
  is not in the left table and does not appear.

## Summary

- `merge` matches on a key column. The default `inner` drops the unmatched;
  use `how="left"` when adding information.
- `indicator=True` shows the unmatched; `validate=` stops a row explosion in
  advance. Check the row count after merging.
- Key types must be equal; different names use `left_on` / `right_on`,
  same-named columns `suffixes`.
- `concat` stacks (`ignore_index`, `keys`), `join` matches on the index.
