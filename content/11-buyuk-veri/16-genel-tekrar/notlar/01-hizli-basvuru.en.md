The track's most used code on one page, with section numbers.

## Measuring (1)

```python
df.info(memory_usage="deep")
df.memory_usage(deep=True).sum() / 1024**2      # MB
os.path.getsize("orders.csv") / 1024**2         # MB on disk

tracemalloc.start()
...
peak = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()
```

## Types (2)

```python
pd.read_csv("orders.csv", dtype={"quantity": "int8", "city": "category"},
            parse_dates=["order_time"])
pd.to_numeric(df["quantity"], downcast="integer")
df["city"] = df["city"].astype("category")
df["quantity"].min(), df["quantity"].max()      # look before overflowing
```

## In chunks (3)

```python
total, count = 0.0, 0
for chunk in pd.read_csv("orders.csv", chunksize=250_000):
    total += chunk["unit_price"].sum()
    count += len(chunk)
mean = total / count
```

## Parquet (4, 5)

```python
df.to_parquet("orders.parquet", compression="zstd", row_group_size=100_000)
pd.read_parquet("orders.parquet", columns=["city"])

pf = pq.ParquetFile("orders.parquet")
pf.metadata.num_rows, pf.num_row_groups
pf.metadata.row_group(0).column(0).statistics   # min, max
pf.read_row_group(0, columns=["city"])

writer = pq.ParquetWriter("out.parquet", table.schema, compression="zstd")
writer.write_table(table)
writer.close()
```

## Partitioning (6)

```python
for month, part in df.groupby("month"):
    os.makedirs(f"lake/month={month}", exist_ok=True)
    part.drop(columns="month").to_parquet(f"lake/month={month}/part-0.parquet")
```

## DuckDB (7, 8)

```python
duckdb.sql("FROM 'orders.parquet' LIMIT 5")
duckdb.sql("DESCRIBE FROM 'orders.csv'")
duckdb.sql("SUMMARIZE FROM 'orders.parquet'")
duckdb.sql("FROM read_parquet('lake/*/*.parquet', hive_partitioning = true)")
duckdb.sql("SELECT * FROM df").df()             # a pandas table by name
duckdb.execute("SELECT ... WHERE city = ?", ["Ankara"]).fetchall()
duckdb.sql("COPY (SELECT ...) TO 'result.parquet'")
```

## Sampling (9)

```python
df.sample(n=10_000, random_state=1)
df.groupby("city").sample(n=500, random_state=1)    # stratified
se = sample["x"].std() / len(sample) ** 0.5         # standard error
```

## Parallel and dask (10, 11)

```python
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(work, items))

import dask.dataframe as dd
ddf = dd.read_csv("orders-*.csv")
ddf.groupby("city")["unit_price"].mean().compute()
```

## MapReduce and Spark (12, 13)

```python
zlib.crc32(key.encode()) % n_machines          # stable spreading

rdd.map(f).filter(g).reduceByKey(lambda a, b: a + b).collect()
rdd.cache()
df.groupBy("city").agg({"revenue": "sum"}).show()
```

## Streaming data (14)

```python
start = event["ts"] // 60 * 60                  # tumbling window
while times[0] <= event["ts"] - 60:              # sliding window
    times.popleft()
if start + 60 <= newest - lateness:              # watermark: too late
    ...
if event["event_id"] in seen:                    # a copy
    continue
```
