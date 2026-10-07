# Overall Review

You have reached the end of the Big Data track. You started with the question
"the file does not fit in memory"; now you can measure and shrink data, store
it in a form that suits the questions, process it with all the cores on one
machine, and you know what changes when you move to many machines or to a
live stream. This section walks the road from start to end once more: at
every stop, the most important idea and the code you will use most.

<figure class="fig">
  <div class="flow">
    <span class="node">Measure, shrink<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">Files<br><small>04–06</small></span><span class="arrow">→</span>
    <span class="node">DuckDB<br><small>07–09</small></span><span class="arrow">→</span>
    <span class="node">Cores<br><small>10–11</small></span><span class="arrow">→</span>
    <span class="node acc">Cluster, stream<br><small>12–14</small></span>
  </div>
  <figcaption>The road of the Big Data track: first working smarter on the same machine, then many machines and live data.</figcaption>
</figure>

## 1. What big means, how to measure (Sections 0–1)

Data is **big** if it is too much for the machine and tool that process it;
there is no fixed limit. Disk is big and lasting, memory small and fast;
pandas reads a file into memory from start to end. The file size does not
tell you the size in memory: the 61 MB orders CSV is 96 MB in memory.

```python
df.info(memory_usage="deep")          # summary and real size
df.memory_usage(deep=True)            # bytes per column
tracemalloc.start()                   # peak memory
time.perf_counter()                   # time
```

Whether a program crashes is decided by the **peak memory**, not the final
size. First try working smarter on the same machine (vertical), then more
machines (horizontal).

## 2. Shrinking with types (Section 2)

| Column | Type | Watch out |
|---|---|---|
| Small integer | `int8`, `int16`, `int32` | Overflow is silent: `astype("int8")` turns 300 into 44 |
| Decimal | `float32` | ~7 digits; not for money |
| Text with few values | `category` | Harmful if almost all differ |
| Date | `datetime64` | `pd.to_datetime` or `parse_dates` |
| Integer with gaps | `Int8` … `Int64` | With a capital letter |

Best of all is giving the types **while reading**:
`read_csv(dtype=..., parse_dates=...)`. A million orders went from 95.9 MB to
22.9 MB.

## 3. Reading in chunks (Section 3)

```python
for chunk in pd.read_csv("orders.csv", chunksize=250_000):
    ...  # summarise the chunk
```

The pattern: **summarise each chunk, combine the summaries.** Total, count,
smallest and largest combine directly; for a mean, the total and the count
are gathered separately and divided at the end (the mean of means is wrong).
Different values combine with a `set`; the median cannot be found exactly
from chunks.

## 4. File formats and Parquet (Sections 4–5)

CSV is text, row by row and without types. **Parquet** is columnar: it reads
only the columns needed, keeps the types and compresses well.

```python
df.to_parquet("orders.parquet", compression="zstd", row_group_size=100_000)
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
pf = pq.ParquetFile("orders.parquet")    # metadata, read_row_group
```

Inside the file: row groups → column chunks; the footer holds the smallest
and largest value of every column in every group. Groups that clearly cannot
match a condition are skipped without being read, but only if the data is
**sorted** by that column.

## 5. Partitioning (Section 6)

```text
orders/month=2024-03/part-0.parquet
```

When data is split into folders by a column that is often filtered on,
folders that do not match the condition are never opened (**partition
pruning**). The partition column should have few values: splitting too finely
leads to the small files problem. New data is added as a new folder.

## 6. DuckDB (Sections 7–8)

```python
import duckdb

duckdb.sql("SELECT city, count(*) FROM 'orders.parquet' GROUP BY city")
duckdb.sql("FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)")
duckdb.sql("SELECT * FROM orders")                   # a pandas table, by name
duckdb.execute("... WHERE city = ?", ["Ankara"])     # a value from outside
```

A server-free analysis database inside Python: it queries a file like a
table and reads only the columns needed, with all the cores. Give the big work
to DuckDB and the small result to pandas (`.df()`). A value from outside is
passed with `?`, never pasted into the text.

## 7. Sampling and approximation (Section 9)

- `df.sample(n=..., random_state=...)`: the seed makes the result repeatable.
- Standard error = standard deviation / √n; the error depends on the **size
  of the sample**, not of the whole data.
- Regular picks such as `head` are biased; when comparing groups, use a
  stratified sample.
- Approximate distinct counts (HyperLogLog) and percentiles work with constant
  memory; they are not used where an exact value is needed.

## 8. All the cores: parallel and dask (Sections 10–11)

| Tool | When |
|---|---|
| `ProcessPoolExecutor` | Pure Python calculation (processes to get past the GIL) |
| `ThreadPoolExecutor` | Waiting jobs, NumPy |
| dask DataFrame | pandas syntax, data bigger than memory |
| `dask.delayed` | Making any function lazy and parallel |

Code that uses processes must be under `if __name__ == "__main__":`.
Parallelism has a cost: for small jobs and jobs that send big data it was
slower than sequential. dask is lazy: until `compute()`, only a task graph is
built.

## 9. Many machines: MapReduce and Spark (Sections 12–13)

**MapReduce** has three steps: map (record → key–value), shuffle (the same key
to the same place), reduce (a key's values → a result). The combiner added up
in advance on each machine and cut the data crossing the network from a
million pairs to 32. Keys are spread over machines with a stable hash
(`zlib.crc32`; Python's `hash()` differs in every process).

**Spark** keeps intermediate results in memory and offers a rich, lazy
language:

```python
counts = (lines.flatMap(lambda line: line.split())
               .map(lambda word: (word, 1))
               .reduceByKey(lambda a, b: a + b))   # transformations: a recipe
counts.collect()                                    # an action: run it
```

A narrow transformation stays inside the partition, a wide one needs a
shuffle; an RDD used twice is computed once with `cache()`; a big result is
not `collect()`ed to the driver but written to disk.

## 10. Streaming data (Section 14)

- A stream has no end; events are not kept, a small **state** is updated.
- **Windows:** tumbling (`ts // 60 * 60`), sliding (the last N seconds,
  `deque`), session (closed by a gap).
- Windows are built on **event time**; for late events, a **watermark**:
  waiting little gives an incomplete result, waiting long a late one.
- With at-least-once delivery, copies are removed by id (idempotence).
- **Kafka:** topic, partition, offset, commit; order only inside a partition.

## Which tool?

| Situation | Tool |
|---|---|
| Fits in memory easily | pandas (with the right types) |
| Bigger than memory, a one-off summary | `chunksize` |
| Will be queried every day | Parquet + partitioning |
| SQL on files, one machine | DuckDB |
| pandas syntax, bigger than memory | dask |
| A quick idea is enough | Sampling, approximate counts |
| Many machines | Spark |
| Data arrives live | Streaming: windows, Kafka |

## All the pieces together (Section 15)

The pipeline in the capstone project used almost every section of the track:
first a memory estimate from a sample (1, 2), converting the CSV to Parquet
piece by piece (3, 5), partitioning by month (6), querying with DuckDB and
reading only one of 12 files for a question about one month (7), checking the
result with partial totals from row groups (12), and a sample for a quick
estimate (9). If you can say why each step is there, this track has reached
its goal.

## What comes next?

This track taught you to deal with the **size** of data. On the Data Engineer
route the next steps are turning this pipeline into a service others can use
(the API tracks) and packaging it to run the same on every computer (Docker).
If you are heading for machine learning, the measuring, sampling and checking
you learned here apply just the same when choosing the data that goes into a
model from a large data set.
