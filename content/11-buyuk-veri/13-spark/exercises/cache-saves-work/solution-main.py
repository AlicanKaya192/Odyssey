from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

nums = sc.parallelize(range(1_000), 4)

plain = nums.map(lambda x: x * 2)
before = sc.stats.partitions_computed
plain.count()
plain_sum = plain.sum()
print(sc.stats.partitions_computed - before)

cached = nums.map(lambda x: x * 2).cache()
before = sc.stats.partitions_computed
cached.count()
cached_sum = cached.sum()
print(sc.stats.partitions_computed - before)

print(plain_sum == cached_sum)
