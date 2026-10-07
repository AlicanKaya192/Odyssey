# Measuring Memory

In the last section we looked at how much room the **whole** table takes. To
shrink something that is not enough; the real question is: **which column**
is expensive, and **why**? In this section you will learn to measure a table
column by column, the index's share, how much new memory an operation opens,
and how to catch the highest memory moment of your code.

All the examples use the table of 100 000 orders:

```python
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 100_000)
df = pd.read_csv("orders.csv")
```

## `info`: a summary at a glance

`df.info()` shows the skeleton of the table: the number of rows, the
columns, each column's type and the number of non-empty values. With
`memory_usage="deep"` it also writes the real memory use at the bottom:

```python
df.info(memory_usage="deep")
```

```text
<class 'pandas.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype  
---  ------       --------------   -----  
 0   order_id     100000 non-null  int64  
 1   order_time   100000 non-null  str    
 2   customer_id  100000 non-null  int64  
 3   city         100000 non-null  str    
 4   category     100000 non-null  str    
 5   quantity     100000 non-null  int64  
 6   unit_price   100000 non-null  float64
 7   payment      100000 non-null  str    
dtypes: float64(1), int64(3), str(4)
memory usage: 9.6 MB
```

Line by line:

- `RangeIndex: 100000 entries`: 100 000 rows, the index from 0 to 99 999.
- For each column, `Non-Null Count` (the number of non-empty values) and
  `Dtype` (the type). `int64` and `float64` are numbers, `str` is text.
- `dtypes: float64(1), int64(3), str(4)`: how many columns of each type.
- `memory usage: 9.6 MB`: the room the table takes in memory.

`info` is a quick first look. But it does not say how much each column
takes; for that you need the next tool.

## Column by column: `memory_usage`

```python
print(df.memory_usage(deep=True))
```

```text
Index              132
order_id        800000
order_time     2700000
customer_id     800000
city           1446549
category       1426855
quantity        800000
unit_price      800000
payment        1279540
dtype: int64
```

The result is a series: the number of **bytes** for each column. `Index` on
the first line is the table's index; it is not a column, but it takes room
too (we will look at it shortly).

The numeric columns are exactly 800 000 bytes: 100 000 rows × 8 bytes. The
text columns are all different. Why?

## Why is text expensive?

A number is always 8 bytes, but text takes as much room as it is long.
pandas 3 stores each text cell in two parts:

- the characters of the text itself: 8 bytes for `"Istanbul"` (English
  letters take one byte each; letters such as `ş` and `ğ` take two),
- an **8-byte** marker that shows where the text starts.

Every value in the `order_time` column is 19 characters, like
`"2024-04-11 21:41:26"`. 19 + 8 = 27 bytes; over 100 000 rows, 2 700 000
bytes. The most expensive column in the table is a date, but a date stored
**as text**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>42</code> (<code>int64</code>)</span><span>8 bytes, always</span></div>
    <div class="anat-row"><span><code>"card"</code></span><span>4 characters + an 8-byte marker = 12 bytes</span></div>
    <div class="anat-row"><span><code>"Istanbul"</code></span><span>8 characters + 8 = 16 bytes</span></div>
    <div class="anat-row"><span><code>"2024-04-11 21:41:26"</code></span><span>19 characters + 8 = 27 bytes</span></div>
  </div>
  <figcaption>In pandas 3 a text cell takes as many bytes as it has characters, plus an 8-byte marker that shows where it starts. Long text, expensive column.</figcaption>
</figure>

Let us turn this into a report per column:

```python
memory = df.memory_usage(deep=True).drop("Index")
report = pd.DataFrame({
    "mb": (memory / 1024**2).round(2),
    "share": (memory / memory.sum() * 100).round(1),
    "per_row": (memory / len(df)).round(1),
})
print(report.sort_values("mb", ascending=False))
```

```text
               mb  share  per_row
order_time   2.57   26.9     27.0
city         1.38   14.4     14.5
category     1.36   14.2     14.3
payment      1.22   12.7     12.8
customer_id  0.76    8.0      8.0
order_id     0.76    8.0      8.0
quantity     0.76    8.0      8.0
unit_price   0.76    8.0      8.0
```

- `mb`: the column's megabytes.
- `share`: what percentage of the table it is.
- `per_row`: bytes per row.

The report says three things:

1. The four text columns are **more than two thirds** of the table
   (26.9 + 14.4 + 14.2 + 12.7 = 68.2%).
2. `order_time` alone is a quarter; stored as a date it would drop to 8
   bytes.
3. `city`, `category` and `payment` repeat the same few words on every row
   (`Istanbul`, `card` and so on). There is a far cheaper way to store
   repeated text.

The fix for the second and third points is the subject of the next section.
For now what matters is this: you now know **with a number** what to
shrink.

## When does `deep=True` make a difference?

With pandas 3's `str` type the result is the same whether or not you write
`deep=True`; pandas already knows the size of the text. But if the text was
read the old way, as the `object` type, things change:

```python
df = pd.read_csv("orders.csv", dtype={"city": object})
print(df["city"].memory_usage())
print(df["city"].memory_usage(deep=True))
```

```text
800132
5546681
```

An `object` column holds the **address** of a Python object in every cell.
Without `deep`, pandas counts only the addresses: 8 bytes × 100 000. With the
text objects included, the real size is about seven times more. If you are
measuring someone else's code, an old pandas or an `object` column, do not
forget `deep=True`; otherwise the result tells you only part of the truth.

## The index takes room too

The table's index lives in memory as well. The index `read_csv` gives you is
a `RangeIndex`: it does not store the numbers from 0 to 99 999 one by one, it
keeps only the "start, stop, step" triple. That is why it is 132 bytes.

If you make a column the index, that can change:

```python
from orders_data import make_orders

df = make_orders(100_000)
a = df.set_index("order_id")
b = df.set_index("customer_id")
print(type(a.index).__name__, a.memory_usage(deep=True)["Index"])
print(type(b.index).__name__, b.memory_usage(deep=True)["Index"])
```

```text
RangeIndex 132
Index 800000
```

`order_id` goes up in order, 1, 2, 3, …; pandas notices this and builds a
`RangeIndex` again. `customer_id` holds mixed numbers; each one is stored
separately: 8 bytes per row. Keep this in mind when you choose an index.

## Operations open new memory

Every operation on a table leaves a mark in memory. Let us write a small
measuring function and look step by step:

```python
def mb(frame):
    return round(frame.memory_usage(deep=True).sum() / 1024**2, 1)

df = pd.read_csv("orders.csv")
print("start:   ", mb(df))
df["total"] = df["quantity"] * df["unit_price"]
print("+ total: ", mb(df))
istanbul = df[df["city"] == "Istanbul"]
print("istanbul:", mb(istanbul), len(istanbul))
copy = df.copy()
print("copy:    ", mb(copy))
```

```text
start:    9.6
+ total:  10.4
istanbul: 3.9 34196
copy:     10.4
```

- A new numeric column: 8 more bytes per row (9.6 → 10.4 MB).
- Filtering (`df[...]`) produces **a new table**: 3.9 MB more for the
  Istanbul orders. `df` stays in memory too.
- `copy()` builds the whole table once more.

An important idea comes out of this: **peak memory**. Even if the table is
small at the end of an operation, **while** the operation runs the old and
the new are in memory at the same time. Whether a program crashes is decided
not by the size at the end but by this peak.

<figure class="fig">
  <div class="flow">
    <span class="node"><code>a</code> built<br>7.6 MB</span><span class="arrow">→</span>
    <span class="node acc"><code>b = a * 2</code><br>both at once: 15.3 MB</span><span class="arrow">→</span>
    <span class="node"><code>del a</code><br>only <code>b</code>: 7.6 MB</span>
  </div>
  <figcaption>The use at the end is 7.6 MB but the peak is 15.3 MB. With 10 MB of memory the program would crash at the middle step.</figcaption>
</figure>

## Catching the peak: `tracemalloc`

The `tracemalloc` module from Python's standard library watches the memory
allocated from the moment it is switched on and gives two numbers: the
**current** use and the **peak** so far.

```python
import tracemalloc
import numpy as np

tracemalloc.start()
a = np.arange(1_000_000)
b = a * 2
del a
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(round(current / 1024**2, 1), round(peak / 1024**2, 1))
```

```text
7.6 15.3
```

At the end only `b` is left: 7.6 MB. But while `a * 2` was being worked out
`a` was in memory too; the peak is the two arrays together, 15.3 MB.
`del a` deletes a name; if no other name uses that object, it also frees the
memory.

The steps:

1. `tracemalloc.start()`: start watching.
2. Run the code you want to measure.
3. `tracemalloc.get_traced_memory()`: a `(current, peak)` pair, in bytes.
4. `tracemalloc.stop()`: stop watching (watching slows the code a little).

> **Careful:** `tracemalloc` only sees allocations that go through Python's
> own memory manager: Python objects and NumPy arrays. pandas 3's `str`
> columns live in the memory of a separate library (Arrow), and
> `tracemalloc` does not count them. For the size of a table use
> `memory_usage(deep=True)`; for the peak of an operation, `tracemalloc`.

## Measuring time

With big data, **time** matters as much as memory. In Python you measure
how long a piece of code takes with `time.perf_counter()`: read the clock
before and after the work and take the difference.

```python
import time

start = time.perf_counter()
df = pd.read_csv("orders.csv")
print(round(time.perf_counter() - start, 2), "s")

start = time.perf_counter()
df = pd.read_csv("orders.csv", usecols=["city", "unit_price"])
print(round(time.perf_counter() - start, 2), "s")
```

On a file of a million rows, on this computer, the first read took 0.84
seconds and reading only two columns (`usecols`) took 0.32 seconds. On your
computer the numbers will be different; time depends on the processor, the
disk and the other programs running at that moment. So:

- Measure time **several times**; the first run is often slower.
- Compare two ways **on the same computer, one after the other**.
- Look at the **ratio**, not the absolute number: "it took a third as
  long".

Reading only the columns you need with `usecols` cuts both time and
memory. Section 3 covers it in detail.

## The measuring habit

When you meet new data:

1. `df.info(memory_usage="deep")`: the overall picture.
2. `df.memory_usage(deep=True)`: which column is expensive?
3. Bytes per row: how much more than 8 are the text columns?
4. Before a heavy operation: what will the peak be? How many copies will
   be in memory at once?

## Summary

- `df.info(memory_usage="deep")` gives a summary of the table and its real
  size.
- `df.memory_usage(deep=True)` gives bytes per column; the `Index` row is
  the index's share.
- A numeric column takes 8 bytes per row; a `str` column the number of
  characters + 8 bytes. In this table the text columns are 68% of the
  memory.
- `deep=True` really matters for `object` columns: without it only the
  addresses are counted.
- A `RangeIndex` takes almost no room; an index of mixed numbers takes 8
  bytes per row.
- Filtering and `copy()` produce new tables. Whether a program crashes is
  decided not by the size at the end but by **peak memory**, measured with
  `tracemalloc`.
- Measure time with `time.perf_counter()` and make comparisons on the same
  computer.
