A MultiIndex is not only for rows. When `agg` gets more than one function per
column, the **columns** get two levels and writing something like
`report["sales_sum"]` in the next step fails.

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa"],
    "sales": [80, 95, 120, 110, 50],
    "returns": [2, 5, 4, 1, 0],
})
report = df.groupby("city").agg({"sales": ["sum", "mean"], "returns": ["sum"]})
print(report.columns.tolist())
print(report)
print(report[("sales", "sum")].tolist())
report.columns = ["_".join(pair) for pair in report.columns]
print(report.columns.tolist())
named = df.groupby("city").agg(total=("sales", "sum"), avg=("sales", "mean"))
print(named.columns.tolist())
```

```text
[('sales', 'sum'), ('sales', 'mean'), ('returns', 'sum')]
       sales        returns
         sum   mean     sum
city                       
Ankara   230  115.0       5
Bursa     50   50.0       0
Izmir    175   87.5       7
[230, 50, 175]
['sales_sum', 'sales_mean', 'returns_sum']
['total', 'avg']
```

## Three ways

1. **Selecting with a tuple:** the column name is now the tuple
   `("sales", "sum")`. `report[("sales", "sum")]` works, but writing tuples
   everywhere is tiring.
2. **Flattening:** `"_".join(pair)` turns each tuple into one name:
   `sales_sum`, `sales_mean`, `returns_sum`. If the report goes to CSV or
   Excel this is the cleanest way; a two-row header looks bad there.
3. **Named aggregation:** `agg(total=("sales", "sum"), ...)` gives single-level
   columns from the start and you choose the names. This is the recommended
   form in new code.

## When are MultiIndex columns good?

When you want to see the same measures side by side for many groups (total
and average for each city), a two-level header is readable and
`report["sales"]` brings both columns in one move. But if the table goes to
another tool or a model, flatten it.
