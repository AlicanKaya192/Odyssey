Taking a single column out of a table is one of the most common steps in
data work.

**What you need to do:**

1. The `records` list is ready in the starter code.
2. Collect the `city` value of every record into a list and keep it in a
   variable called `cities`. Keep the original order.
3. Print the `cities` list.
4. Print how many **distinct** cities there are.

**Expected output:**

```
['Ankara', 'Izmir', 'Ankara', 'Izmir', 'Bursa']
3
```

In pandas this will be `data["city"]` and `data["city"].nunique()`.
