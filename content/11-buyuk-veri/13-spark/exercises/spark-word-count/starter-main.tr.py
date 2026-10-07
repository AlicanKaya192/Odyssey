from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext

text = [
    "spark keeps data in memory",
    "spark splits data into partitions",
    "data moves in a shuffle",
    "memory makes spark fast",
]

# Kelime sayma ve siralama.


# Ilk dort ve farkli kelime sayisi.
