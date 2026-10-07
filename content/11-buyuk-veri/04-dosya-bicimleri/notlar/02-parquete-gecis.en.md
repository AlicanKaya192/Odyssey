You have a CSV and want to move it to Parquet. The steps, and the traps
tried on this machine.

## 1. Give the types correctly, once

```python
df = pd.read_csv(
    "orders.csv",
    dtype={"city": "category", "category": "category", "payment": "category",
           "quantity": "int8"},
    parse_dates=["order_time"],
)
df.to_parquet("orders.parquet", compression="zstd")
```

Since Parquet stores the types, this work is done **once**. From then on
every `read_parquet` brings the types ready.

## 2. Look inside the file

`pyarrow.parquet` gives a summary of the file without reading it:

```python
import pyarrow.parquet as pq

f = pq.ParquetFile("orders.parquet")
print(f.metadata.num_rows, f.metadata.num_columns, f.metadata.num_row_groups)
print(f.schema_arrow)
```

The number of rows, the columns and their types, the number of row groups.
We open up row groups in the next section.

## 3. Read only what you need

```python
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
```

## Traps

**`to_parquet` does not append, it writes from scratch.** Writing 100 rows
and then 50 rows to the same file left 50 rows in the file. To write Parquet
in pieces, either write each piece to a separate file (Section 6) or use
`pyarrow.parquet.ParquetWriter` (Section 5).

**The index is stored.** A table written with `set_index("customer_id")`
comes back with `customer_id` as its index; in the file that index sits as a
column (it shows up last in the `schema_arrow.names` list). The default
`RangeIndex`, on the other hand, is stored only as a piece of information and
takes no column.

**A binary file.** It does not open in Notepad and cannot be checked by eye;
to look inside, use `pq.ParquetFile` above or `pd.read_parquet(...).head()`.

**Categories come back with their type.** Categories come back from Parquet
as `category`; the list of categories is stored in the file.
