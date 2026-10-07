# Partitioned Data

In the last section we saw Parquet skip the row groups **inside** a file using
statistics. Partitioning takes the same idea one step further: you split the
data into **separate files and folders** by the value of a column. The
reading program knows which file it needs without opening it, just by looking
at the **folder name**.

Almost every big data system stores data this way: a company's sales piled up
over years do not sit in one file but in day or month folders.

The examples work with a million orders; we put each order's month in a
column:

```python
from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(1_000_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df["month"] = df["order_time"].dt.strftime("%Y-%m")
```

## The folder layout

Data partitioned by month looks like this on disk:

<figure class="fig">
<pre><code class="language-text">orders/
├─ month=2024-01/
│  └─ part-0.parquet
├─ month=2024-02/
│  └─ part-0.parquet
├─ month=2024-03/
│  └─ part-0.parquet
└─ ... (12 folders)</code></pre>
  <figcaption>Each month in its own folder. The folder name <code>month=2024-03</code> tells the month of every row inside; the month column is not in the files.</figcaption>
</figure>

The folder names have the form `column=value`: `month=2024-03`. This way of
writing comes from the Hive tool in the Hadoop world, and today almost every
tool recognises it (pandas, Spark, DuckDB). A folder's name carries a piece of
information for every row in it: "every order here is from March 2024".

## Partitioning by hand

To see the mechanism, let us do it ourselves first: split by month with
`groupby` and write each month to its own folder.

```python
for month, part in df.groupby("month"):
    folder = Path("orders") / f"month={month}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="month").to_parquet(folder / "part-0.parquet", index=False)

files = sorted(Path("orders").rglob("*.parquet"))
print(len(files))
for f in files[:3]:
    print(f.as_posix(), round(f.stat().st_size / 1024**2, 2))
```

```text
12
orders/month=2024-01/part-0.parquet 2.22
orders/month=2024-02/part-0.parquet 2.08
orders/month=2024-03/part-0.parquet 2.22
```

- `groupby("month")` gives a `(month, that month's rows)` pair for each month.
- `Path("orders") / f"month={month}"` builds the folder's path;
  `mkdir(parents=True, exist_ok=True)` creates the folder (and its parents if
  needed) and raises no error if it exists.
- We do not put the `month` column in the file: the information is already in
  the folder's name.
- `rglob("*.parquet")` finds every Parquet file inside the folder, including
  subfolders.

The twelve files add up to 26.2 MB; the same data was 20.9 MB in one file.
Each file carries its own dictionary and footer, so partitioning costs a
little space.

## Reading only the folder you need

The March orders are needed. With partitioned data only one file is opened;
with a single file all of it is read and filtered:

```python
march = pd.read_parquet("orders/month=2024-03/part-0.parquet")

whole = pd.read_parquet("all.parquet")
march2 = whole[whole["order_time"].dt.month == 3]
```

Both give 84 836 orders. On this computer the first took 0.009 seconds and
the second 0.077 seconds: about **eight times**. As the data grows, so does
the part that is not read; as long as you want one month, you read one month.

This skipping is called **partition pruning**: partitions that do not match
the condition are eliminated by looking only at their names, without opening
their files.

<figure class="fig">
  <div class="flow">
    <span class="node">Condition<br><code>month = 2024-03</code></span><span class="arrow">→</span>
    <span class="node">Look at folder names</span><span class="arrow">→</span>
    <span class="node">Drop 11 folders</span><span class="arrow">→</span>
    <span class="node acc">Read one file</span>
  </div>
  <figcaption>Partition pruning: the files in the dropped folders are never opened.</figcaption>
</figure>

## Letting pandas do it: `partition_cols`

Partitioning by hand shows the mechanism; in everyday work `to_parquet` can do
it by itself:

```python
df.to_parquet("by_month", partition_cols=["month"], index=False)
```

```text
by_month/month=2024-01/b4ee06afe85b42749f2cd20b49999f3c-0.parquet
by_month/month=2024-02/...
```

The file names are random (different on every write); the folder names
follow the same layout. When reading, giving the folder itself is enough, and
`filters=` does the partition pruning by itself:

```python
back = pd.read_parquet("by_month")
march = pd.read_parquet("by_month", filters=[("month", "==", "2024-03")])
```

In `back` the `month` column comes back; pandas rebuilds it from the folder
names and makes it a `category`.

Like `filters=` in the last section, `partition_cols` and reading a folder use
the `pyarrow.dataset` module behind the scenes. In an installation where that
module cannot be loaded these forms raise an error; the by-hand method in
this section then works everywhere.

## How finely should you split?

Twelve files by month went well. What if we split by day?

| Split | Files | Total | Reading all |
|---|---|---|---|
| One file | 1 | 20.9 MB | 0.069 s |
| By month | 12 | 26.2 MB | — |
| By day | 366 | 28.1 MB | 1.09 s |

Reading all 366 small files is **fifteen times** slower than one file: opening
each file, reading its footer and joining the results is separate work. This
is a well-known problem in the big data world: **small files**. If we tried
splitting by customer there would be 245 461 folders.

When choosing a partition column:

1. It should be a column you **filter on often** (time, country, source).
2. It should have **few different values**: dozens, at most a few thousand.
3. Each partition should be **big enough**. In large systems the common
   advice is tens to hundreds of megabytes per file.

For a table of a million orders the month is more than enough; with billions
of rows, day or hour becomes suitable.

## Adding new data

Partitioning has one more win: when a new month arrives you add **only a new
folder**, without touching the old files. Let `january_2025` be the table of
January 2025 orders:

```python
folder = Path("orders") / "month=2025-01"
folder.mkdir(parents=True, exist_ok=True)
january_2025.to_parquet(folder / "part-0.parquet", index=False)
```

To read the last two months we look at the folder names and rebuild the month
from them:

```python
parts = []
for f in sorted(Path("orders").glob("month=*/*.parquet")):
    month = f.parent.name.split("=")[1]
    if month >= "2024-12":
        p = pd.read_parquet(f)
        p["month"] = month
        parts.append(p)
recent = pd.concat(parts, ignore_index=True)
print(recent.groupby("month").size().to_dict())
```

```text
{'2024-12': 85002, '2025-01': 6750}
```

- `f.parent.name` is the name of the folder the file is in: `month=2024-12`.
- `split("=")[1]` takes what comes after the equals sign: `2024-12`.
- `"2024-12" >= "2024-12"`: months written as `YYYY-MM` also sort correctly as
  text.

The month column was not in the files; we put it back from the folder name.
When reading with `partition_cols`, pandas does the same work itself.

## Splitting into buckets

Filtering by customer is a common job too: "all the orders of customer 1234".
But 245 461 customers are too many to open folders for. The solution: spread
the customer number over a **fixed number of buckets**.

```python
df["bucket"] = df["customer_id"] % 8
print(df["bucket"].value_counts().sort_index().tolist())
```

```text
[124749, 124952, 124796, 125218, 125315, 124915, 125034, 125021]
```

`%` gives the remainder of a division: each customer falls into exactly one
bucket from 0 to 7, and the buckets are almost equal in size. All of a
customer's orders are **in the same bucket**; to find them only one file out
of eight is read (`1234 % 8 = 2` → bucket 2). This method is called
**bucketing** (or *hash partitioning*); Spark and data warehouses use it too.

## Summary

- Partitioning splits the data into separate folders by the value of a
  column: `orders/month=2024-03/part-0.parquet`.
- When reading, folders that do not match the condition are eliminated
  without being opened (**partition pruning**); in this measurement reading a
  month was eight times faster.
- By hand: `groupby` + `to_parquet` of each part into its own folder. Letting
  pandas do it: `to_parquet(..., partition_cols=[...])` and
  `read_parquet(folder, filters=...)`.
- The partition column should be one you filter on often, with few values;
  splitting too finely leads to the **small files** problem (366 files,
  fifteen times slower).
- New data is added as a new folder; the old ones are not rewritten.
- For columns with many values, a fixed number of buckets:
  `customer_id % 8`.
