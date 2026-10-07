The most commonly used operations of Spark (and `minispark`).

## Getting started

```python
# real Spark: from pyspark.sql import SparkSession
from minispark import SparkSession
spark = SparkSession.builder.appName("app").getOrCreate()
sc = spark.sparkContext
```

## RDD transformations (lazy)

| Operation | What it does | Kind |
|---|---|---|
| `map(f)` | `f` on every item | narrow |
| `filter(f)` | the items where `f` is true | narrow |
| `flatMap(f)` | many items from each item | narrow |
| `mapValues(f)` | `f` on only the value of a `(k, v)` pair | narrow |
| `keys()`, `values()` | a pair's key / value | narrow |
| `reduceByKey(f)` | combine per key (in the partition first) | wide |
| `groupByKey()` | a list of values per key | wide |
| `distinct()` | items without repeats | wide |
| `sortBy(f)` | sort | wide |

## RDD actions (they run)

| Operation | Returns |
|---|---|
| `collect()` | all items, a list |
| `count()` | the number of items |
| `take(n)`, `first()` | the first n items / the first item |
| `reduce(f)` | the items brought down to one value with `f` |
| `sum()` | the total |

## Other

```python
rdd.getNumPartitions()      # the number of partitions
rdd.glom().collect()        # inside the partitions
rdd.cache()                 # keep in memory the first time it is computed
rdd.toDebugString()         # the lineage
```

## DataFrame

```python
df = spark.createDataFrame(pandas_df, numPartitions=4)
df.withColumn("revenue", "quantity * unit_price")
df.filter("quantity >= 4")
df.select("city", "revenue")
df.groupBy("city").agg({"revenue": "sum", "unit_price": "avg"})
df.orderBy("city")
df.show(); df.count(); df.toPandas()
df.explain()
df.createOrReplaceTempView("orders"); spark.sql("SELECT ...")
```

## Differences between `minispark` and real PySpark

| `minispark` | PySpark |
|---|---|
| `df.filter("quantity >= 4")` | `df.filter(df.quantity >= 4)` or the same text |
| `df.withColumn("r", "quantity * unit_price")` | `df.withColumn("r", df.quantity * df.unit_price)` |
| `agg({"revenue": "sum"})` | the same, or `F.sum("revenue")` |
| A single process | A cluster (driver + executors) |
| SQL with DuckDB behind it | Spark's own SQL engine |

## Installing real Spark

1. Install Java (a version such as JDK 17).
2. `pip install pyspark`.
3. Run the same code with `from pyspark.sql import SparkSession`; with
   `local[*]` it uses all the cores on a single machine.
