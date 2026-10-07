from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

# The numbers 1-20, 4 partitions.


# Number of partitions and items in each partition.


# The total of the squares of the even numbers.
