# File Formats

So far we have always read data from CSV. CSV is everywhere and every program
can open it, but for big data it is one of the most expensive formats. In this
section we write the same million orders to disk in five different formats
and compare them. The differences are striking: the file size ranges from
159 MB to 14 MB, and reading takes anywhere from 3 seconds to a few hundredths
of a second.

The table we compare with is a million orders prepared with the right types,
as in the last section:

```python
import pandas as pd
from orders_data import make_orders

df = make_orders(1_000_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")
```

## CSV: the language everyone speaks

CSV (*comma-separated values*) is a plain text file: each line is a record,
the values are separated by commas, the first line holds the column names.

```python
make_orders(3).to_csv("o.csv", index=False)
print(open("o.csv").read())
```

```text
order_id,order_time,customer_id,city,category,quantity,unit_price,payment
1,2024-01-02 22:15:01,8,Ankara,toys,3,234.3,card
2,2024-07-01 22:07:37,2,Istanbul,clothing,1,443.5,card
3,2024-11-30 00:28:55,8,Istanbul,clothing,5,367.51,transfer
```

**Strengths:** it opens even in Notepad, every language and program can read
it, and it can be checked by eye.

**Weaknesses:**

1. **The text is parsed on every read.** The text `"234.3"` has to be turned
   into a number; for eight columns over a million rows, eight million times.
2. **Types are lost.** A CSV holds only text; it does not know whether
   something is a date or a category. Let us write the table and read it
   back:

```python
df.to_csv("orders.csv", index=False)
back = pd.read_csv("orders.csv")
print(df["order_time"].dtype, df["city"].dtype)
print(back["order_time"].dtype, back["city"].dtype)
```

```text
datetime64[us] category
str str
```

   The date and the category became text when written and stayed text when
   read. You have to give the types from the last section again on every
   read.

3. **It is laid out row by row.** Even if you want only two columns, every
   line of the file has to be read and split from start to end.

## Compressed CSV

If you add `.gz` to the end of the file name, pandas compresses the file with
**gzip** as it writes, and opens it by itself when reading:

```python
df.to_csv("orders.csv.gz", index=False)
back = pd.read_csv("orders.csv.gz")
```

The file went from 61.1 MB to 15.2 MB. But writing went up from 1.3 seconds
to 3.5 seconds and reading got a little slower: first it has to be opened,
then the text parsed as before. A good choice if disk or network is tight; the
problems of types and row layout stay exactly as they were.

## JSON Lines: for nested data

JSON Lines (`.jsonl`) writes one JSON object per line:

```python
small = make_orders(3)[["order_id", "city", "unit_price"]]
small.to_json("o.jsonl", orient="records", lines=True)
print(open("o.jsonl").read())
```

```text
{"order_id":1,"city":"Ankara","unit_price":234.3}
{"order_id":2,"city":"Istanbul","unit_price":443.5}
{"order_id":3,"city":"Istanbul","unit_price":367.51}
```

Data from APIs, application logs and nested structures (such as a list of
products inside an order) often come in this form. To read it,
`pd.read_json("o.jsonl", lines=True)`.

The price: **the column names repeat on every line**. For a million orders
the file is 159.3 MB, two and a half times the CSV, and it is the slowest to
read (3.25 seconds).

## Rows or columns?

The real difference is in **how the file is laid out**. CSV and JSON lay it
out row by row: first all the values of the first order, then those of the
second. Columnar formats lay it out column by column: first all the
`order_id` values, then all the `city` values.

<figure class="fig">
  <div class="versus">
    <div><h4>Row layout (CSV, JSON)</h4><p><code>1, 2024-01-02, Ankara, toys, 3, 234.3</code><br><code>2, 2024-07-01, Istanbul, clothing, 1, 443.5</code><br><code>3, 2024-11-30, Istanbul, clothing, 5, 367.51</code><br>Every row is read even for two columns.</p></div>
    <div class="ok"><h4>Column layout (Parquet)</h4><p><code>order_id</code>: 1, 2, 3, …<br><code>city</code>: Ankara, Istanbul, Istanbul, …<br><code>unit_price</code>: 234.3, 443.5, 367.51, …<br>Only the requested columns are read.</p></div>
  </div>
  <figcaption>The same three orders in two layouts. In the column layout similar values sit side by side, so it compresses well.</figcaption>
</figure>

This layout has two big wins:

1. **Only the columns you need are read.** "Mean price per city" needs two
   columns; the places where the other six live are never touched.
2. **Similar values sit side by side.** The values in a column have the same
   type and are often alike (`Istanbul`, `Istanbul`, `Ankara`, …); such a run
   compresses very well.

Since most analysis asks "a few columns, many rows" questions, a columnar
format almost always wins for big data.

## Parquet

Parquet is the most common columnar file format: Spark, DuckDB, data
warehouses and cloud storage systems read it directly. In pandas writing and
reading it is one line (the `pyarrow` library works behind the scenes):

```python
df.to_parquet("orders.parquet")
back = pd.read_parquet("orders.parquet")
print(back["order_time"].dtype, back["city"].dtype)
```

```text
datetime64[us] category
```

The types were kept: the date came back as a date, the category as a
category. A Parquet file stores the type of each column inside itself.

To read only a few columns, `columns=`:

```python
prices = pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
```

Parquet is a binary file: open it in Notepad and you see meaningless
characters. It was designed to be read by programs, not people.

### Compression

By default Parquet compresses each column with **snappy**: fast, with
moderate compression. For a smaller file, **zstd**:

```python
df.to_parquet("orders_zstd.parquet", compression="zstd")
```

20.9 MB with snappy, 13.9 MB with zstd. In this measurement both read in the
same time.

## Feather

Feather (the Arrow IPC format) writes the table to disk in a form very close
to its layout in memory. Writing and reading it is very fast:

```python
df.to_feather("orders.feather")
back = pd.read_feather("orders.feather")
```

It is handy as a temporary intermediate file between two Python programs or
between the steps of a job. For data to be shared with other tools or kept
for a long time, Parquet is more common.

## Why not Excel?

An Excel file (`.xlsx`) is the most familiar way to share a table but it does
not suit big data: a sheet can hold at most 1 048 576 rows, and reading and
writing it is even slower than CSV. Our million orders sit just below that
limit.

## Comparison

The same million orders, on this computer:

| Format | Size | Write | Read | Read two columns |
|---|---|---|---|---|
| CSV | 61.1 MB | 1.3 s | 0.84 s | 0.32 s |
| CSV + gzip | 15.2 MB | 3.5 s | 0.92 s | — |
| JSON Lines | 159.3 MB | 1.6 s | 3.25 s | — |
| Parquet (snappy) | 20.9 MB | 0.18 s | 0.02 s | 0.01 s |
| Parquet (zstd) | 13.9 MB | 0.22 s | 0.02 s | — |
| Feather | 22.2 MB | 0.03 s | 0.02 s | — |

The read times are the fastest of three tries. On your computer the numbers
will differ, but the ratios will stay similar: Parquet reads not a few times
but **tens of times** faster than CSV (0.84 seconds against 0.02).

Why such a difference? In CSV every value is parsed from text. In Parquet the
values are already numbers, column by column, with their types; reading is
largely copying from disk into memory.

## Which one when?

- **CSV:** when the data goes to someone else, another program or a person;
  when it is small.
- **CSV + gzip:** CSV is required but the file is big and disk or network is
  tight.
- **JSON Lines:** when the data is nested, or arrives that way from an API
  or a log file.
- **Parquet:** the default choice for storing big data, analysing it and
  sharing it with other big data tools.
- **Feather:** a fast intermediate file between programs on the same
  machine.

For the rest of this track we will mostly keep the data as Parquet.

## Summary

- CSV is text, row by row and typeless: the text is parsed on every read,
  and dates and categories are lost.
- The `.gz` extension brings a CSV down to a quarter but slows writing.
- JSON Lines suits nested data; the column names repeat on every line, so it
  is the biggest file.
- A columnar format reads only the columns you need and compresses well
  because similar values sit side by side.
- Parquet keeps the types, chooses columns with `columns=` and compresses
  with snappy or zstd; in this measurement it read tens of times faster than
  CSV.
- Feather is a fast intermediate file; Excel is not for big data.
