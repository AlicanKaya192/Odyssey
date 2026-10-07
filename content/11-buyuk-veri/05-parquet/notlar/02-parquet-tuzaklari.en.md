Every trap on this page was tried on this machine.

## 1. Not closing the `ParquetWriter`

```python
writer.write_table(table)
pd.read_parquet("orders.parquet")
# ArrowInvalid: ... Parquet magic bytes not found in footer
```

The footer is written by `close()`. Do not forget `writer.close()` after the
loop.

## 2. A schema difference between pieces

A column that arrives as whole numbers in one piece and as decimals in the
next:

```text
ValueError: Table schema does not match schema used to create file
```

Fix the types in `read_csv` with `dtype=` so every piece arrives with the
same types.

## 3. Losing data while forcing the schema

`pa.Table.from_pandas(b, schema=first_schema, safe=False)` **forces** a
different type into the first schema. A decimal 1.5 forced into a
whole-number schema quietly became 1. Do not use `safe=False`; give the right
types from the start.

## 4. Expecting `filters=` to help on unsorted data

`filters=` only skips groups whose statistics cannot match the condition. If
the cities are mixed in every group, `city == "Izmir"` cannot skip any group;
the whole file is still read. Write the data sorted by the column you filter
on most.

## 5. Forgetting the price of sorting

Sorted by city, the file grew from 26.0 MB to 31.7 MB: the time and the order
number, which were in order before, are now mixed. Sorting by one column can
break the order of another.

## 6. Making row groups too small

Reading with groups of 1 000 rows is about three times slower than with
groups of 100 000 (0.121 s against 0.037 s).

## 7. `filters=` is not available in every installation

Behind the scenes `filters=` uses the `pyarrow.dataset` module. If that
module cannot be loaded, this error comes:

```text
ValueError: the 'filters' keyword is not supported when the pyarrow.dataset
module is not available
```

In that case do the skipping by hand: look at the statistics with
`pq.ParquetFile` and read the suitable groups with `read_row_group` (the
December example in the section).

## 8. Putting the index into the file without meaning to

`pa.Table.from_pandas(chunk)` can add the piece's index as a column. When
writing in pieces, `preserve_index=False`.
