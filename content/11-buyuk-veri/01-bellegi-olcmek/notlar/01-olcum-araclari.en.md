All the measuring tools you will use on this track are on this page. They all
return bytes; for megabytes, `/ 1024**2`.

## Table and column

| Code | What it gives |
|---|---|
| `df.info(memory_usage="deep")` | Columns, types, non-empty counts and the real total size |
| `df.memory_usage(deep=True)` | Bytes per column; the first row is `Index` |
| `df.memory_usage(deep=True).sum()` | The whole table |
| `df.memory_usage(deep=True).drop("Index")` | The columns only |
| `df["city"].memory_usage(deep=True)` | One column (index included) |
| `df.index.memory_usage()` | The index only |
| `array.nbytes` | A NumPy array |

## A ready-made report

```python
memory = df.memory_usage(deep=True).drop("Index")
report = pd.DataFrame({
    "mb": (memory / 1024**2).round(2),
    "share": (memory / memory.sum() * 100).round(1),
    "per_row": (memory / len(df)).round(1),
})
print(report.sort_values("mb", ascending=False))
```

If `per_row` is much bigger than 8, the column is either text or the wrong
type.

## A file

```python
import os

os.path.getsize("orders.csv")     # bytes
```

## Peak memory

```python
import tracemalloc

tracemalloc.start()
# ... the code to measure ...
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
```

- `current`: what is allocated right now.
- `peak`: the highest value since `start()`.
- Sees only Python objects and NumPy arrays; does not see pandas 3's `str`
  columns.
- `tracemalloc.reset_peak()`: resets the peak, to measure two operations
  separately in the same session.

## Time

```python
import time

start = time.perf_counter()
# ... the code to measure ...
seconds = time.perf_counter() - start
```

`time.perf_counter()`, not `time.time()`: it measures short durations more
precisely and does not jump when the system clock changes.

## This table's measurements (100 000 orders)

| Column | Type | Bytes per row |
|---|---|---|
| `order_time` | `str` | 27.0 |
| `city` | `str` | 14.5 |
| `category` | `str` | 14.3 |
| `payment` | `str` | 12.8 |
| `order_id`, `customer_id`, `quantity` | `int64` | 8 |
| `unit_price` | `float64` | 8 |

9.6 MB in total; the text columns are 68.2%.
