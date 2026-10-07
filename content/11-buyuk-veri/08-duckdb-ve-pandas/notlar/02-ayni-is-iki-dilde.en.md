The pandas and DuckDB (SQL) versions of the same questions. Which one you
find more readable is also a reason to choose.

## Filtering

```python
orders[(orders["city"] == "Izmir") & (orders["quantity"] >= 3)]
```

```sql
SELECT * FROM orders WHERE city = 'Izmir' AND quantity >= 3
```

## Grouping

```python
orders.groupby("city")["unit_price"].mean()
```

```sql
SELECT city, avg(unit_price) FROM orders GROUP BY city
```

## Several summaries

```python
orders.groupby("city").agg(n=("order_id", "count"), avg_price=("unit_price", "mean"))
```

```sql
SELECT city, count(*) AS n, avg(unit_price) AS avg_price FROM orders GROUP BY city
```

## Joining

```python
orders.merge(customers, on="customer_id")
```

```sql
SELECT * FROM orders JOIN customers USING (customer_id)
```

## The first of each group

```python
orders.sort_values("order_time").groupby("customer_id").head(1)
```

```sql
SELECT * FROM orders
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1
```

## A running total

```python
monthly["revenue"].cumsum()
```

```sql
SELECT month, sum(revenue) OVER (ORDER BY month) FROM monthly
```

## Sorting and the top N

```python
orders.nlargest(5, "unit_price")
```

```sql
SELECT * FROM orders ORDER BY unit_price DESC LIMIT 5
```

## Number of distinct values

```python
orders["customer_id"].nunique()
```

```sql
SELECT count(DISTINCT customer_id) FROM orders
```

## Turning rows into columns

```python
monthly.pivot(index="month", columns="category", values="revenue")
```

DuckDB has `PIVOT` too, but for shaping a small result pandas is usually
more comfortable.
