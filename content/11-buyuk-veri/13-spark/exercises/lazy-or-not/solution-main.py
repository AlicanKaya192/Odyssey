from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

nums = sc.parallelize(range(100), 5)
result = nums.map(lambda x: x * 3).filter(lambda x: x % 2 == 0).map(lambda x: x + 1)

print(sc.stats.jobs, sc.stats.partitions_computed)
print(result.count())
print(sc.stats.jobs, sc.stats.partitions_computed)
