Produce a category report of card-paid orders with a Spark DataFrame, and
check the same result with Spark SQL.

**What to do:**

1. `df = spark.createDataFrame(make_orders(50_000), numPartitions=4)`.
2. Add the `revenue` column (`"quantity * unit_price"`) and filter only those
   with `payment == 'card'`.
3. `groupBy("category").agg({"revenue": "sum", "order_id": "count"})`,
   `orderBy("category")`; take the result with `toPandas()`.
4. Print the category, the number of orders and the revenue (two decimals) on
   each line. The column names are `sum(revenue)` and `count(order_id)`.
5. `df.createOrReplaceTempView("orders")`; find the number of card-paid
   orders with `spark.sql` and print whether it equals the total of the counts
   in the report.

**Expected output:**

```
books 7801 3296344.0
clothing 7974 9775615.22
electronics 5091 28591960.41
home 7090 7561763.12
sports 3610 6548086.31
toys 4357 3315431.27
True
```
