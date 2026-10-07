Read only two columns from a Parquet file and find the mean price per city.

**What to do:**

1. The starter code prepares the typed `df` with 200 000 orders; write it as
   `orders.parquet`.
2. Read only two columns with `columns=["city", "unit_price"]`.
3. Print the list of columns of the table you read.
4. Print the memory of the two-column read and of the whole file, in MB (one
   decimal, `memory_usage(deep=True)`), on one line.
5. Find the mean price per city (`groupby("city", observed=True)`), sort from
   largest to smallest and print the first three cities with their means
   (one decimal).

**Expected output:**

```
['city', 'unit_price']
1.7 8.2
Trabzon 744.1
Izmir 741.4
Istanbul 741.4
```

`observed=True` tells it to group only the categories seen in the data.
