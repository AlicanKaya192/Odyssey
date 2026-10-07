Everything you need to look inside a Parquet file and to read and write it in
pieces.

## Layers

| Layer | What it holds |
|---|---|
| File | Row groups + a footer at the very end |
| Row group | A certain number of rows (e.g. 100 000) |
| Column chunk | A single column within a row group |
| Page | A small part of a column chunk |
| Footer | The schema, where the groups are, each column chunk's statistics |

## Looking at the file

```python
import pyarrow.parquet as pq

f = pq.ParquetFile("orders.parquet")
f.metadata.num_rows
f.metadata.num_row_groups
f.schema_arrow                       # the columns and their types
f.schema_arrow.names                 # the column names

rg = f.metadata.row_group(0)         # row group 0
rg.num_rows
col = rg.column(2)                   # that group's column chunk 2
col.path_in_schema                   # the column's name
col.statistics.min, col.statistics.max
col.statistics.null_count
col.total_compressed_size            # bytes on disk
col.compression                      # SNAPPY, ZSTD ...
```

## Reading

```python
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
f.read_row_group(3).to_pandas()
for batch in f.iter_batches(batch_size=250_000, columns=[...]):
    part = batch.to_pandas()
```

## `filters=`

```python
pd.read_parquet("orders.parquet", filters=[("order_time", ">=", start)])
```

- Each condition is a triple: `(column, operation, value)`.
- Operations: `==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not in`.
- Conditions in one list are joined with **and**:
  `[("city", "==", "Izmir"), ("quantity", ">=", 3)]`.
- A list of lists means **or**:
  `[[("city", "==", "Izmir")], [("city", "==", "Bursa")]]`.

## Writing

```python
df.to_parquet("orders.parquet", row_group_size=100_000, compression="zstd")
```

In pieces:

```python
import pyarrow as pa

writer = None
for chunk in ...:
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter("orders.parquet", table.schema)
    writer.write_table(table)
writer.close()
```

## Row group size (a million orders, on this computer)

| `row_group_size` | Groups | File | Read |
|---|---|---|---|
| 1 000 | 1 000 | 27.1 MB | 0.121 s |
| 10 000 | 100 | 27.1 MB | 0.049 s |
| 100 000 | 10 | 26.0 MB | 0.037 s |
| 1 000 000 | 1 | 20.9 MB | 0.057 s |

Very small groups slow reading down (each group has its own preparation). A
single giant group gives the smallest file but leaves nothing to skip.
Somewhere in between (tens of thousands to hundreds of thousands of rows) is
usually good.
