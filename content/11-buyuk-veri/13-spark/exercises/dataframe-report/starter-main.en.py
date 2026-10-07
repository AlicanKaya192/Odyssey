from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext
from orders_data import make_orders

df = spark.createDataFrame(make_orders(50_000), numPartitions=4)

# revenue, the card filter, the category report.


# The report rows.


# Checking with Spark SQL.
