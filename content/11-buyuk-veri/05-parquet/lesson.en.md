# Parquet

In the last section we saw that Parquet is small and fast. In this section we
look at **why**. The inside of a Parquet file is organised so that the program
reading it can **skip the parts it does not need without opening them**. If
you know this layout you can write the file to suit it, and when reading touch
only what you need.

The examples work with a million orders:

```python
import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(1_000_000)
df["order_time"] = pd.to_datetime(df["order_time"])
```

## The layers of the file

A Parquet file is made of four nested layers:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>File</span><span>Row groups laid out one after another</span></div>
    <div class="anat-row"><span>Row group</span><span>For example 100 000 orders; each group can be read on its own</span></div>
    <div class="anat-row"><span>Column chunk</span><span>A single column in a group: the <code>city</code> values of those 100 000 orders</span></div>
    <div class="anat-row"><span>Page</span><span>A small part of a column chunk; the unit of compression</span></div>
    <div class="anat-row"><span>Footer</span><span>At the end of the file: the schema, where the groups are, each column chunk's smallest and largest value</span></div>
  </div>
  <figcaption>The reading program reads the small footer first, then goes only to the groups and columns it needs.</figcaption>
</figure>

1. The **file** is split into row groups.
2. A **row group** holds a certain number of rows: 100 000 orders, for
   example.
3. Inside a row group each column is a separate **column chunk**: only the
   `city` values of those 100 000 orders, for example.
4. A column chunk is split into small **pages**; these are the unit of
   reading and compression.

At the very end of the file there is a **footer**: where each row group
starts in the file, the type of each column, and **summary statistics** for
each column chunk. The reading program reads this small footer first, then
goes only to the parts it needs.

## Row groups

pandas' `to_parquet` puts a million rows into a single row group by default.
With `row_group_size=` you can ask for smaller groups:

```python
df.to_parquet("default.parquet")
df.to_parquet("orders.parquet", row_group_size=100_000)
for name in ["default.parquet", "orders.parquet"]:
    f = pq.ParquetFile(name)
    print(name, f.metadata.num_row_groups, f.metadata.row_group(0).num_rows)
```

```text
default.parquet 1 1000000
orders.parquet 10 100000
```

`pq.ParquetFile(...)` opens the file but does not read its data; `metadata`
is the summary in the footer. This call is fast whatever the size of the file.

## Each group's statistics

The footer stores the smallest and largest value for every column of every
row group. Let us look at order time, price and city:

```python
f = pq.ParquetFile("orders.parquet")
names = f.schema_arrow.names
t = names.index("order_time")
c = names.index("city")
for i in range(f.metadata.num_row_groups):
    rg = f.metadata.row_group(i)
    times = rg.column(t).statistics
    cities = rg.column(c).statistics
    print(i, times.min.date(), times.max.date(), cities.min, cities.max)
```

```text
0 2024-01-01 2024-02-06 Adana Trabzon
1 2024-02-06 2024-03-14 Adana Trabzon
2 2024-03-14 2024-04-19 Adana Trabzon
3 2024-04-19 2024-05-26 Adana Trabzon
4 2024-05-26 2024-07-02 Adana Trabzon
5 2024-07-02 2024-08-07 Adana Trabzon
6 2024-08-07 2024-09-13 Adana Trabzon
7 2024-09-13 2024-10-19 Adana Trabzon
8 2024-10-19 2024-11-25 Adana Trabzon
9 2024-11-25 2024-12-31 Adana Trabzon
```

- Since the orders were produced in time order, each group holds a separate
  slice of the year: group 0 is early January, group 9 December.
- The cities, on the other hand, are mixed in every group: each group's
  smallest is `Adana` and its largest `Trabzon`.

## Skipping without reading

Suppose you want only the December orders. The statistics make the answer
clear: a group whose largest time is before 1 December **cannot** contain a
December order. There is no need to open those groups.

```python
start = pd.Timestamp("2024-12-01")
keep = [i for i in range(f.metadata.num_row_groups)
        if f.metadata.row_group(i).column(t).statistics.max >= start]
print(keep)
parts = [f.read_row_group(i).to_pandas() for i in keep]
december = pd.concat(parts)
december = december[december["order_time"] >= start]
print(len(december))
```

```text
[9]
85002
```

Only one group out of ten was read. The chosen group also holds rows from
late November, so we filtered once more at the end.

This is called **predicate pushdown**: pushing the condition down towards the
data. `read_parquet` does it by itself with `filters=`:

```python
december = pd.read_parquet(
    "orders.parquet",
    filters=[("order_time", ">=", pd.Timestamp("2024-12-01"))],
)
```

On this computer reading the whole file took 0.036 seconds and reading
December with `filters=` 0.014 seconds. The bigger the file, the bigger the
part that is skipped.

## Order changes everything

Let us try the same trick for the city: "only Izmir". In the statistics every
group runs from `Adana` to `Trabzon`; Izmir **could** be in any group. No
group can be skipped.

If we sort by city before writing the file, things change:

```python
by_city = df.sort_values("city")
by_city.to_parquet("by_city.parquet", row_group_size=100_000)
f2 = pq.ParquetFile("by_city.parquet")
c = f2.schema_arrow.names.index("city")
for i in range(f2.metadata.num_row_groups):
    s = f2.metadata.row_group(i).column(c).statistics
    print(i, s.min, s.max)
```

```text
0 Adana Ankara
1 Ankara Ankara
2 Ankara Antalya
3 Antalya Bursa
4 Bursa Istanbul
5 Istanbul Istanbul
6 Istanbul Istanbul
7 Istanbul Izmir
8 Izmir Konya
9 Konya Trabzon
```

Now Izmir can only be in groups 7 and 8; the other eight groups are skipped.
But it is not free: since the time order was broken, the file grew from
26.0 MB to 31.7 MB (time and order numbers in order compressed better).

The rule: write the file **sorted by the column you filter on most**. For data
such as time series that is usually time anyway.

## Column chunks and dictionary encoding

Let us look inside one row group and see how many bytes each column chunk
takes on disk:

```python
rg = pq.ParquetFile("orders.parquet").metadata.row_group(0)
for j in range(rg.num_columns):
    col = rg.column(j)
    print(col.path_in_schema, col.total_compressed_size)
```

```text
order_id 603354
order_time 848893
customer_id 596194
city 38081
category 38050
quantity 38141
unit_price 532649
payment 25650
```

Over 100 000 rows `city` takes 38 081 bytes and `order_time` 848 893 bytes:
more than twenty times as much. Why? Parquet
stores repeated values with **dictionary encoding**: the list of different
values once, and only their numbers in the rows. It is the file's counterpart
of the `category` type from earlier sections. For `order_time`, where nearly
every value is different, the dictionary does not help.

## Reading in pieces

In Parquet the "pieces" are ready-made: the row groups. Reading one group on
its own:

```python
g = pq.ParquetFile("orders.parquet").read_row_group(3).to_pandas()
print(len(g), g["order_id"].iloc[0], g["order_id"].iloc[-1])
```

```text
100000 300001 400000
```

`iter_batches` hands the file out in pieces of the size you choose; it is the
Parquet counterpart of `read_csv(chunksize=...)`:

```python
total = 0
for batch in pq.ParquetFile("orders.parquet").iter_batches(
        batch_size=250_000, columns=["quantity", "unit_price"]):
    part = batch.to_pandas()
    total += (part["quantity"] * part["unit_price"]).sum()
print(round(total, 2))
```

```text
1635737361.77
```

`columns=` works here too: only two columns are read.

## Writing in pieces: `ParquetWriter`

We saw it in the last section: `to_parquet` does not append to the end of a
file. To turn a CSV that does not fit in memory into a single Parquet file
there is `pyarrow.parquet.ParquetWriter`: you open the file once, write each
piece as a new row group, and close it at the end.

```python
import pyarrow as pa
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
writer = None
for chunk in pd.read_csv("orders.csv", chunksize=200_000, parse_dates=["order_time"]):
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema)
    writer.write_table(table)
writer.close()
```

- `pa.Table.from_pandas(...)`: turns a pandas table into `pyarrow`'s own
  table type. `preserve_index=False` keeps the index out of the file.
- `table.schema`: the columns and their types. The writer is opened with the
  first piece's schema.
- Each `write_table` adds a row group: a million rows, five groups.
- `writer.close()` writes the footer. If you try to read before closing you
  get `ArrowInvalid: ... Parquet magic bytes not found in footer`: there is
  no footer at the end of the file yet.

Memory holds one piece at any moment, however big the CSV.

Each piece's schema must be **the same** as the first. If a column arrives as
whole numbers in one piece and as decimals in another, `write_table` raises
an error: `ValueError: Table schema does not match schema used to create
file`. To prevent it, fix the types in `read_csv` with `dtype=`.

## Summary

- Parquet: file → row groups → column chunks → pages; at the end a footer
  holding the types and statistics.
- `pq.ParquetFile(path).metadata` gives row, group and column information
  without reading the file.
- `row_group_size=` chooses the size of the row groups.
- The smallest and largest value is stored for every column of every group;
  groups that clearly cannot match the condition are skipped without reading
  (`filters=`).
- Skipping only works if the data is **sorted** by the filtered column;
  sorting can change compression.
- Repeated values take very little room thanks to dictionary encoding.
- Read in pieces with `read_row_group` and `iter_batches`; write in pieces
  with `ParquetWriter`, with the same schema in every piece.
