from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

# Three transformations.


# Counters, the action, counters.
