Aynı soruların pandas ve DuckDB (SQL) karşılıkları. Hangisini daha okunur
bulduğun da bir seçim ölçütü.

## Süzmek

```python
orders[(orders["city"] == "Izmir") & (orders["quantity"] >= 3)]
```

```sql
SELECT * FROM orders WHERE city = 'Izmir' AND quantity >= 3
```

## Gruplamak

```python
orders.groupby("city")["unit_price"].mean()
```

```sql
SELECT city, avg(unit_price) FROM orders GROUP BY city
```

## Birden çok özet

```python
orders.groupby("city").agg(n=("order_id", "count"), avg_price=("unit_price", "mean"))
```

```sql
SELECT city, count(*) AS n, avg(unit_price) AS avg_price FROM orders GROUP BY city
```

## Birleştirmek

```python
orders.merge(customers, on="customer_id")
```

```sql
SELECT * FROM orders JOIN customers USING (customer_id)
```

## Her grubun ilki

```python
orders.sort_values("order_time").groupby("customer_id").head(1)
```

```sql
SELECT * FROM orders
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1
```

## Birikimli toplam

```python
monthly["revenue"].cumsum()
```

```sql
SELECT month, sum(revenue) OVER (ORDER BY month) FROM monthly
```

## Sıralayıp ilk N

```python
orders.nlargest(5, "unit_price")
```

```sql
SELECT * FROM orders ORDER BY unit_price DESC LIMIT 5
```

## Farklı değer sayısı

```python
orders["customer_id"].nunique()
```

```sql
SELECT count(DISTINCT customer_id) FROM orders
```

## Satırları sütuna çevirmek

```python
monthly.pivot(index="month", columns="category", values="revenue")
```

DuckDB'de de `PIVOT` var, ama küçük bir sonucu biçimlendirmek için pandas
çoğu zaman daha rahat.
