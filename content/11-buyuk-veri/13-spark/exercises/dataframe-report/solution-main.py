from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext
from orders_data import make_orders

df = spark.createDataFrame(make_orders(50_000), numPartitions=4)

card = df.withColumn("revenue", "quantity * unit_price").filter("payment == 'card'")
report = (card.groupBy("category")
              .agg({"revenue": "sum", "order_id": "count"})
              .orderBy("category")
              .toPandas())

for row in report.itertuples(index=False):
    print(row.category, row[2], round(row[1], 2))

df.createOrReplaceTempView("orders")
n = spark.sql("SELECT count(*) AS n FROM orders WHERE payment = 'card'").toPandas()["n"][0]
print(n == report["count(order_id)"].sum())
