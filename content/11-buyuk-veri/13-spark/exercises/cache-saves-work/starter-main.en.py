from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

nums = sc.parallelize(range(1_000), 4)

# Without a cache: two actions and the increase in the counter.


# With a cache: two actions and the increase in the counter.


# Are the two totals the same?
