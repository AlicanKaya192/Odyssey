from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

nums = sc.parallelize(range(1, 21), 4)

print(nums.getNumPartitions())
print(nums.glom().map(len).collect())

print(nums.filter(lambda x: x % 2 == 0).map(lambda x: x * x).sum())
