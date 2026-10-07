# Reading in Chunks

With the right types the table got four times smaller. But what if the file
is 200 GB? Even four times smaller it is 50 GB; it still will not fit on most
computers.

When you read a long book you do not spread every page across your desk at
once. You read a page, note what you need to remember, and turn the page. At
any moment the desk holds one page and a small notebook.

In this section we read the file the same way: **in chunks**. At any moment
memory will hold just one chunk and a small intermediate result. This is
called *out-of-core* processing: the data as a whole never enters memory.

The examples in this section work with the file of a million orders:

```python
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
```

## Take a look first: `nrows`

When you meet a big file, the first job is not to read it from start to end
but to look at its first few rows. `nrows` reads only that many rows:

```python
print(pd.read_csv("orders.csv", nrows=3).to_string(index=False))
```

```text
 order_id          order_time  customer_id     city category  quantity  unit_price  payment
        1 2024-01-01 00:00:47        45209 Istanbul     toys         2      207.09 transfer
        2 2024-01-01 00:01:01        86038  Trabzon clothing         1      437.73     card
        3 2024-01-01 00:02:18        64622    Konya clothing         2      283.38     card
```

Column names, the form of the values, how the date is written: you can decide
on types and columns without reading the whole file.

## `chunksize`: split the file into chunks

When you give `read_csv` a `chunksize=`, it does not return a table; it
returns **a reader**. Looping over the reader with `for` brings one chunk at
each step:

```python
reader = pd.read_csv("orders.csv", chunksize=100_000)
print(type(reader).__name__)
for i, chunk in enumerate(reader):
    print(i, len(chunk), chunk["order_id"].iloc[0], chunk["order_id"].iloc[-1])
```

```text
TextFileReader
0 100000 1 100000
1 100000 100001 200000
2 100000 200001 300000
3 100000 300001 400000
4 100000 400001 500000
5 100000 500001 600000
6 100000 600001 700000
7 100000 700001 800000
8 100000 800001 900000
9 100000 900001 1000000
```

- Each `chunk` is an ordinary `DataFrame`; you can do everything you know
  with it.
- A chunk is 100 000 rows: about 9.6 MB in memory. The whole file is 96 MB.
- A reader can be looped over once; to go through it again, call `read_csv`
  again.

<figure class="fig">
  <div class="flow">
    <span class="node">Read</span><span class="arrow">→</span>
    <span class="node">Summarise</span><span class="arrow">→</span>
    <span class="node">Note it down</span><span class="arrow">→</span>
    <span class="node">Let it go</span><span class="arrow">→</span>
    <span class="node acc">Result</span>
  </div>
  <figcaption>The first four steps repeat for every chunk; when the chunks run out, the result comes from the notebook. At any moment memory holds one chunk and a small notebook.</figcaption>
</figure>

## Accumulating: a total from chunks

Let us work out the revenue (quantity × price) of all orders with chunks. The
idea is simple: work out each chunk's total and **accumulate** it in a
variable.

```python
total = 0
rows = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    revenue = chunk["quantity"] * chunk["unit_price"]
    total += revenue.sum()
    rows += len(chunk)
print(rows, round(total, 2))
```

```text
1000000 1635737361.77
```

Had we read the whole file and worked it out, the result would be exactly the
same: 1 635 737 361.77. But memory never held more than one chunk.

`total` and `rows` are the small notebook carried through the loop: after
each chunk all we keep is two numbers.

## Trap 1: the mean of means

Suppose we want the mean price with chunks. The first idea is to take each
chunk's mean and then the mean of those. Let us make the chunk size 300 000
(the last chunk will have 100 000 rows):

```python
means = []
total = 0
count = 0
for chunk in pd.read_csv("orders.csv", chunksize=300_000):
    means.append(float(chunk["unit_price"].mean()))
    total += chunk["unit_price"].sum()
    count += len(chunk)
print([round(m, 2) for m in means])
print(round(sum(means) / len(means), 4))
print(round(total / count, 4))
```

```text
[737.47, 737.53, 736.77, 733.38]
736.287
736.869
```

The two results differ. The real mean (from the whole file) is 736.869. The
mean of means is wrong because it gives the last chunk of 100 000 rows as
much weight as the chunks of 300 000.

The right way: accumulate **the total and the count** separately and divide
at the very end. Means cannot be combined; totals and counts can.

## Grouping with chunks

Let us find the revenue per city with chunks. In each chunk we take the total
per city with `groupby` and put it in a list; at the end we join the chunk
results and add them up once more:

```python
parts = []
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    chunk["revenue"] = chunk["quantity"] * chunk["unit_price"]
    parts.append(chunk.groupby("city")["revenue"].sum())

combined = pd.concat(parts).groupby(level=0).sum()
print((combined / 1e6).round(2).sort_values(ascending=False))
```

```text
city
Istanbul    557.00
Ankara      260.83
Izmir       212.50
Bursa       147.92
Antalya     146.01
Adana       115.39
Konya       114.42
Trabzon      81.66
Name: revenue, dtype: float64
```

- `parts` holds 10 small series, each with 8 rows (8 cities). They take
  almost no room in memory.
- `pd.concat(parts)` makes one series of 80 rows; each city appears 10
  times.
- `groupby(level=0).sum()` adds up once more by the index (the city name).

The pattern has two steps: **summarise in the chunk, then combine the
summaries.** Totals, counts, minimums and maximums all fit this pattern.

## Trap 2: counting distinct values

How many different customers are there? Adding up each chunk's `nunique()` is
wrong:

```python
seen = set()
wrong = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000, usecols=["customer_id"]):
    seen.update(chunk["customer_id"])
    wrong += chunk["customer_id"].nunique()
print(len(seen))
print(wrong)
```

```text
245461
824660
```

The same customer ordered in many chunks; counting per chunk counts one
person many times. The right way is to collect the customers you have seen in
a `set`: a set holds each value once. But there is a price: the set keeps
every different customer in memory. If the number of different values is huge,
that may not fit either.

The **median** is harder still: there is no relationship between each
chunk's median and the median of the whole. Finding the median exactly needs
all the values. Ways to get an approximate result are in Section 9.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Total, count, minimum, maximum</span><span>Combine directly: add, or take the smallest / largest</span></div>
    <div class="anat-row"><span>Mean</span><span>Accumulate the total and the count, divide at the end</span></div>
    <div class="anat-row"><span>Number of distinct values</span><span>Collect the values seen in a set</span></div>
    <div class="anat-row"><span>Median, percentiles</span><span>Cannot be found exactly from chunks</span></div>
  </div>
  <figcaption>The check question: if I knew the result for two chunks, could I find the result for the two together?</figcaption>
</figure>

## Filtering and keeping a small result

Often you do not need the whole file, only part of it. You can filter each
chunk and accumulate what is left:

```python
pieces = []
for chunk in pd.read_csv("orders.csv", chunksize=100_000):
    pieces.append(chunk[chunk["category"] == "electronics"])
electronics = pd.concat(pieces, ignore_index=True)
print(len(electronics), round(electronics.memory_usage(deep=True).sum() / 1024**2, 1))
```

```text
139775 14.1
```

Out of a million rows, 139 775 electronics orders remained: 14.1 MB. As long
as the result fits in memory this works. `ignore_index=True` drops the chunks'
old indexes and gives a new index starting at 0.

## Writing the result in chunks too

If even the filtered result is too big for memory, do not accumulate it;
**append** each chunk's result to a file:

```python
first = True
for chunk in pd.read_csv("orders.csv", chunksize=250_000):
    big = chunk[chunk["quantity"] >= 4]
    big.to_csv("big_orders.csv", mode="w" if first else "a", header=first, index=False)
    first = False
```

- `mode="w"`: for the first chunk, write the file from scratch.
- `mode="a"`: for later chunks, add to the end of the file (*append*).
- `header=first`: the column names only once, at the top.

With this pattern the job gets done even when neither the input nor the output
ever fits in memory.

## How much memory do chunks save?

Let us work out the revenue two ways with only the two numeric columns and
look at the peak with `tracemalloc`:

```python
import tracemalloc

columns = ["quantity", "unit_price"]

tracemalloc.start()
total = 0
for chunk in pd.read_csv("orders.csv", chunksize=100_000, usecols=columns):
    total += (chunk["quantity"] * chunk["unit_price"]).sum()
print("chunks peak", round(tracemalloc.get_traced_memory()[1] / 1024**2, 1))
tracemalloc.stop()

tracemalloc.start()
df = pd.read_csv("orders.csv", usecols=columns)
total = (df["quantity"] * df["unit_price"]).sum()
print("full peak", round(tracemalloc.get_traced_memory()[1] / 1024**2, 1))
tracemalloc.stop()
```

```text
chunks peak 4.7
full peak 23.8
```

With chunks the peak is 4.7 MB, all at once 23.8 MB. Reading all at once,
the peak grows with the file; reading in chunks, it stays at the size of one
chunk, because the previous chunk is let go before the next one arrives. That
is the real strength of chunked reading: **memory depends not on the size of
the file but on the size of the chunk.**

(Here we read only the numeric columns with `usecols`; `tracemalloc` sees
numeric columns but not text columns.)

## How big should a chunk be?

I measured the same city revenue calculation with different chunk sizes on
this computer:

| Way | Time |
|---|---|
| All at once | 0.89 s |
| Chunks of 10 000 rows | 1.23 s |
| Chunks of 100 000 rows | 0.96 s |
| Chunks of 500 000 rows | 0.89 s |

Very small chunks are slow: pandas has a fixed amount of preparation for
each chunk, and with 100 chunks of 10 000 rows that work is done 100 times. As
the chunk grows, the time approaches that of reading all at once. The rule:
make a chunk **small enough to fit comfortably in memory and big enough to
make the preparation negligible**. Chunks of a few tens of megabytes are
usually a good start: in this table 100 000 rows is about 10 MB.

## Without pandas: reading row by row

Python can already read a file row by row. With the `csv` module from the
standard library each row arrives as a dictionary:

```python
import csv

total = 0.0
with open("orders.csv", newline="") as f:
    for row in csv.DictReader(f):
        total += int(row["quantity"]) * float(row["unit_price"])
print(round(total, 2))
```

```text
1635737361.77
```

The same result. Memory holds one row at any moment; however big the file,
memory does not change. The price is speed: on this computer 1.74 seconds,
against 0.96 seconds with pandas chunks. Every value is turned from text into
a number one by one in Python (`int(...)`, `float(...)`).

How the `for row in ...` loop works matters: the file object and
`csv.DictReader` do not put all the rows in a list; at each step they produce
**the next** row. In Python such objects are called **iterators**. pandas'
`chunksize` reader is the same idea, only it produces chunks instead of rows.

## Summary

- Look at a few rows first with `nrows=`.
- `chunksize=` gives a reader; each step brings a `DataFrame` chunk. Memory
  depends on the chunk, not the file.
- The pattern: **summarise in the chunk, combine the summaries.** Totals,
  counts, minimums and maximums combine directly.
- The mean of means is wrong: accumulate the total and the count separately
  and divide at the end.
- Per-chunk `nunique()` does not add up; combine with a `set`. The median
  cannot be found exactly from chunks.
- If the filtered result is small use `pd.concat`; if it is big, append to a
  file with `to_csv(mode="a")`.
- Very small chunks are slow; a few tens of megabytes is a good start.
- Reading row by row with the `csv` module works at any size, but is slower.
