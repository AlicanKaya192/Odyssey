from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

text = [
    "spark keeps data in memory",
    "spark splits data into partitions",
    "data moves in a shuffle",
    "memory makes spark fast",
]

# Count the words and sort.


# The first four and the number of different words.
