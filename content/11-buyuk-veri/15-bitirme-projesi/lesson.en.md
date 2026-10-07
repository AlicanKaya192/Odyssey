# Capstone Project

In this section we bring the track's tools together in a single job. There
is no new idea; the aim is to live through, once and from start to end, **in
what order and based on what** decisions are made when you meet a large data
set.

## The scenario

Every night a shop hands over all of the year's orders as a CSV file: a
million rows. The manager asks:

1. What is each month's revenue, city by city?
2. Can we answer such questions every day, without waiting?
3. Can we trust the results?

We have a single laptop. What we build is called a **data pipeline**: a
series of steps that takes raw data and makes it ready for questions.

<figure class="fig">
  <div class="flow">
    <span class="node">Measure</span><span class="arrow">→</span>
    <span class="node">Parquet</span><span class="arrow">→</span>
    <span class="node">Partition</span><span class="arrow">→</span>
    <span class="node">Query</span><span class="arrow">→</span>
    <span class="node acc">Check</span>
  </div>
  <figcaption>Each step uses the output of the one before; behind every step is a section of the track.</figcaption>
</figure>

## 1. Measure first

Section 1's rule: do not guess, measure. Before opening the whole file we
look at its size and at the memory of a small sample:

```python
import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
print(round(os.path.getsize("orders.csv") / 1024**2, 1), "MB on disk")

sample = pd.read_csv("orders.csv", nrows=10_000)
per_row = sample.memory_usage(deep=True).sum() / len(sample)
print(round(per_row * 1_000_000 / 1024**2, 1), "MB in memory (estimate)")
```

```text
61.1 MB on disk
95.9 MB in memory (estimate)
```

The memory per row of ten thousand rows, multiplied by a million, gives an
estimate for the whole. It is bigger than the file on disk: text columns take
up room in memory (Section 1).

The same estimate with the types from Section 2:

```python
DTYPES = {"order_id": "int32", "customer_id": "int32", "quantity": "int8",
          "city": "category", "category": "category", "payment": "category"}
typed = pd.read_csv("orders.csv", nrows=10_000, dtype=DTYPES)
per_row = typed.memory_usage(deep=True).sum() / len(typed)
print(round(per_row * 1_000_000 / 1024**2, 1), "MB with types (estimate)")
```

```text
44.9 MB with types (estimate)
```

Memory drops to less than half. The estimate is reliable too: reading the
whole file with these types gives 44.8 MB. **Decision:** this
size fits in memory, but reading the same CSV from the start every day is
wasted work. We will turn the data, once, into a form that suits the
questions.

## 2. Convert to Parquet, piece by piece

Instead of opening the CSV in one go, we read it in pieces of 250 000 rows
(Section 3) and write a single Parquet file (Section 5). Each piece becomes a
row group in the file. We also add the month column at this point; the next
step will split by it.

```python
import pyarrow as pa
import pyarrow.parquet as pq

NUMERIC = {"order_id": "int32", "customer_id": "int32", "quantity": "int8"}
writer = None
for chunk in pd.read_csv("orders.csv", chunksize=250_000, dtype=NUMERIC):
    chunk["month"] = chunk["order_time"].str[:7]
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema, compression="zstd")
    writer.write_table(table)
writer.close()

pf = pq.ParquetFile("orders.parquet")
print(pf.metadata.num_rows, "rows,", pf.num_row_groups, "row groups")
print(round(os.path.getsize("orders.parquet") / 1024**2, 1), "MB")
```

```text
1000000 rows, 4 row groups
16.4 MB
```

Only one piece is in memory at a time; if the file had a billion rows, the
code would stay the same. The Parquet file is less than a third of the CSV.
We did not give the text columns `category`: Parquet already encodes
repeated values with a dictionary (Section 5).

## 3. Partition by month

Most questions start with "this month". If we split the data into month
folders (Section 6), a question about one month reads only that month's file:

```python
orders = pd.read_parquet("orders.parquet")
for month, part in orders.groupby("month"):
    folder = f"lake/month={month}"
    os.makedirs(folder, exist_ok=True)
    part.drop(columns="month").to_parquet(f"{folder}/part-0.parquet", index=False)

print(sorted(os.listdir("lake"))[:3], len(os.listdir("lake")))
```

```text
['month=2024-01', 'month=2024-02', 'month=2024-03'] 12
```

A folder name like `month=2024-01` is Hive partitioning: the month column is
not inside the file but in the folder's name. A folder layout like this is
also called a **data lake**.

## 4. Query with DuckDB

We query the lake with DuckDB as if it were a single table (Section 7):

```python
import duckdb

lake = "read_parquet('lake/*/*.parquet', hive_partitioning = true)"
print(duckdb.sql(f"""
    SELECT city, round(sum(quantity * unit_price), 2) AS revenue
    FROM {lake}
    WHERE month = '2024-03'
    GROUP BY city
    ORDER BY revenue DESC
    LIMIT 3
""").fetchall())
```

```text
[('Istanbul', 47440696.91), ('Ankara', 22131451.91), ('Izmir', 17415485.42)]
```

We can see from its plan that DuckDB really reads a single folder.
`EXPLAIN ANALYZE` runs the query and gives the details of every step as a long
text. From that text we take only the information about the files scanned,
with `re.search`: `re.search` looks for a pattern in a text, and `\d+` in the
pattern means "one or more digits".

```python
import re

plan = duckdb.sql(f"""
    EXPLAIN ANALYZE SELECT count(*) FROM {lake} WHERE month = '2024-03'
""").fetchall()[0][1]
print(re.search(r"Scanning Files: \d+/\d+", plan).group())
```

```text
Scanning Files: 1/12
```

One file out of twelve. As the data grows, for example to ten years, a
question about one month still reads one file.

## 5. Check

Before giving a number to the manager we also work it out **another way**.
As the second way we read the Parquet file's row groups one by one, produce
partial totals per city and combine them: the same as Section 12's combiner.
Then we compare with DuckDB's result:

```python
totals = {}
for i in range(pf.num_row_groups):
    part = pf.read_row_group(i, columns=["city", "quantity", "unit_price"]).to_pandas()
    part["revenue"] = part["quantity"] * part["unit_price"]
    for city, value in part.groupby("city")["revenue"].sum().items():
        totals[city] = totals.get(city, 0.0) + value

exact = dict(duckdb.sql("""
    SELECT city, sum(quantity * unit_price) FROM 'orders.parquet' GROUP BY city
""").fetchall())
print(all(abs(totals[c] - exact[c]) < 0.01 for c in exact))
print(len(totals), "cities")
```

```text
True
8 cities
```

The two ways give the same result. We compared with "the difference is less
than 0.01" instead of `==`: adding decimal numbers in a different order can
leave very small differences in the last digits.

The second side of checking is a **quick estimate**. Sometimes the manager
wants not the exact number but a quick idea. The sampling from Section 9
estimates the mean order amount per category from one percent of the data:

```python
orders["revenue"] = orders["quantity"] * orders["unit_price"]
sample = orders.sample(frac=0.01, random_state=1)
estimate = sample.groupby("category")["revenue"].mean()
true = orders.groupby("category")["revenue"].mean()
print(((estimate - true).abs() / true * 100).round(1))
```

```text
category
books          0.1
clothing       2.9
electronics    1.5
home           2.1
sports         0.1
toys           2.5
Name: revenue, dtype: float64
```

In this sample the errors are a few percent. Enough for a quick idea; for a
report that will be published, the exact query is run.

## Which step, which section?

| Step | What we did | Section |
|---|---|---|
| Measure | Memory estimate from a sample | 1 |
| Types | `int32`, `int8`, `category` | 2 |
| Piece by piece | Reading with `chunksize` | 3 |
| Parquet | Row groups, `zstd` | 4, 5 |
| Partition | Month folders | 6 |
| Query | DuckDB, SQL on files | 7, 8 |
| Estimate | A 1% sample | 9 |
| Check | Partial totals + combining | 12 |

## Growing the project

This pipeline ran on a single computer. When conditions change, the steps
stay the same; only the tool changes:

- **If the data grows a hundred times:** the converting and partitioning
  steps are done by dask (Section 11) or a Spark cluster (Section 13);
  Parquet and partitioning stay the same.
- **If orders arrive live:** instead of a nightly CSV, a Kafka topic; live
  questions with windows (Section 14), and at the end of the day the events
  are still written to the Parquet lake.
- **If the data lives in the cloud:** the lake sits in cloud storage (such as
  Amazon S3); DuckDB and Spark can read the Parquet files there with the same
  syntax.

The most important decision of this pipeline was at the first step:
**measuring**. A million rows fit into this computer's memory; even so,
partitioning and Parquet made every day's question cheap. Big data is not a
size but a habit: measure first, then read only what is needed.

## Summary

- A data pipeline: measure → convert → partition → query → check.
- When measuring, estimate from a small sample; with types, memory fell to
  less than half.
- Converting a CSV to Parquet piece by piece keeps memory constant and makes
  the file smaller.
- With month folders, a question about one month reads only one of 12 files.
- Check every result another way; compare decimals with a tolerance.
- A sample for a quick estimate, the exact query for a report.
