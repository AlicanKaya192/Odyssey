Spark'ın (ve `minispark`'ın) en sık kullanılan işlemleri.

## Başlamak

```python
# gerçek Spark: from pyspark.sql import SparkSession
from minispark import SparkSession
spark = SparkSession.builder.appName("app").getOrCreate()
sc = spark.sparkContext
```

## RDD dönüşümleri (tembel)

| İşlem | Ne yapar | Tür |
|---|---|---|
| `map(f)` | her öğeye `f` | dar |
| `filter(f)` | `f` doğru olanlar | dar |
| `flatMap(f)` | her öğeden birçok öğe | dar |
| `mapValues(f)` | `(k, v)` çiftinde yalnızca değere `f` | dar |
| `keys()`, `values()` | çiftin anahtarı / değeri | dar |
| `reduceByKey(f)` | anahtar başına birleştir (önce bölümde) | geniş |
| `groupByKey()` | anahtar başına değer listesi | geniş |
| `distinct()` | tekrarsız öğeler | geniş |
| `sortBy(f)` | sırala | geniş |

## RDD eylemleri (çalıştırır)

| İşlem | Döndürür |
|---|---|
| `collect()` | bütün öğeler, liste |
| `count()` | öğe sayısı |
| `take(n)`, `first()` | ilk n öğe / ilk öğe |
| `reduce(f)` | öğeleri `f` ile tek değere indir |
| `sum()` | toplam |

## Diğer

```python
rdd.getNumPartitions()      # bölüm sayısı
rdd.glom().collect()        # bölümlerin içi
rdd.cache()                 # ilk hesaplanışta bellekte tut
rdd.toDebugString()         # soy ağacı
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

## `minispark` ile gerçek PySpark farkları

| `minispark` | PySpark |
|---|---|
| `df.filter("quantity >= 4")` | `df.filter(df.quantity >= 4)` ya da aynı metin |
| `df.withColumn("r", "quantity * unit_price")` | `df.withColumn("r", df.quantity * df.unit_price)` |
| `agg({"revenue": "sum"})` | aynı, ya da `F.sum("revenue")` |
| Tek süreç | Küme (sürücü + yürütücüler) |
| SQL arkada DuckDB | Spark'ın kendi SQL motoru |

## Gerçek Spark'ı kurmak

1. Java (JDK 17 gibi bir sürüm) kur.
2. `pip install pyspark`.
3. `from pyspark.sql import SparkSession` ile aynı kodu çalıştır;
   `local[*]` ile tek makinede bütün çekirdekleri kullanır.
